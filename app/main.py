import os, itertools, concurrent.futures
from concurrent.futures import ThreadPoolExecutor
from datetime import date, datetime, timezone
from flask import Flask, request, jsonify
from core import (
    logger,
    init_pg_db,
    SessionLocal,
    save_to_firestore,
    update_firestore_status,
    init_fs_db,
    MIGRATED_FORM_TYPES,
)
from jobs.commcare_to_postgresql import (
    AttendanceFullOrchestrator as AFJob,
    AttendanceLightOrchestrator as ALJob,
    ObservationOrchestrator as OBJob,
    FarmVisitOrchestrator as FVJob,
    ParticipantRegistrationAndUpdateOrchestrator as PJob,
    WetmillRegistrationOrchestrator as WRJob,
    WetmillVisitOrchestrator as WVJob,
)
from google.cloud.firestore import FieldFilter
from google.cloud import firestore
from google.api_core.retry import Retry
from dotenv import load_dotenv

load_dotenv()

SYSTEM_ID = os.getenv("SYSTEM_USER_ID_TEST")  # Change when deploying to GCP
MAX_RETRIES = 3

app = Flask(__name__)
fs_db = init_fs_db()


def main():
    """Main entry point for initializing the app"""
    init_pg_db()
    logger.info({"message": "Database initialized!"})


# -------------------------------------
# JOB MAPPING
# -------------------------------------
job_mapping = {
    "Farmer Registration": PJob,
    "Attendance Full - Current Module": AFJob,
    "Attendance Full - WIL": AFJob,
    "Edit Farmer Details": PJob,
    "Training Observation": OBJob,
    "Attendance Light - Current Module": ALJob,
    "Demo Plot Observation": OBJob,
    "Farm Visit Full": FVJob,
    "Farm Visit - AA": FVJob,
    "Field Day Farmer Registration": PJob,
    "Field Day Attendance Full": AFJob,
    "Wet Mill Registration Form": WRJob,
    "Wet Mill Visit": WVJob,
}


# -------------------------------------
# SAVE PAYLOAD
# -------------------------------------
@app.route("/save-payload/<source>", methods=["POST"])
def save_payload(source: str):
    """Webhook to receive data and store in Firestore"""
    payload = request.get_json()
    if not payload:
        return jsonify({"error": "Invalid JSON payload"}), 400

    job_name = _extract_job_name(source, payload)
    if not job_name:
        return jsonify({"error": "Job name not provided"}), 422

    request_id = payload.get("id")
    collection = _get_collection(source)

    try:
        if job_name in MIGRATED_FORM_TYPES:
            existing = (
                fs_db.collection(collection)
                .where(filter=FieldFilter("job_id", "==", request_id))
                .limit(1)
                .get()
            )

            if existing:
                doc_id = existing[0].id
                update_firestore_status(
                    doc_id=doc_id,
                    status="new",
                    collection=collection,
                    fields={
                        "payload": payload,
                        "job_name": job_name,
                        "run_retries": 0,
                        "updated_at": firestore.SERVER_TIMESTAMP,
                    },
                )
            else:
                doc_id = save_to_firestore(payload, job_name, "new", collection)

            logger.info(
                {
                    "message": "Payload stored",
                    "job_name": job_name,
                    "doc_id": doc_id,
                    "job_id": request_id,
                }
            )
            return (
                jsonify(
                    {
                        "status": "stored",
                        "job_name": job_name,
                        "doc_id": doc_id,
                        "job_id": request_id,
                    }
                ),
                200,
            )
        else:
            logger.warning(
                {"message": "Job skipped", "job_name": job_name, "job_id": request_id}
            )
            return jsonify({"status": "skipped", "job_name": job_name, "job_id": request_id}), 200

    except Exception as e:
        logger.error(
            {"message": "Failed to save payload", "job_id": request_id, "error": str(e)}
        )
        return jsonify({"error": str(e)}), 500

# -------------------------------------
# SAVE PAYLOAD (BULK)
# -------------------------------------
@app.route("/save-payloads/<source>", methods=["POST"])
def save_payloads(source: str):
    """Bulk save endpoint to receive JSON with multiple payloads"""
    
    payloads = request.get_json(silent=True) or []
    if not payloads:
        return jsonify({"error": "No payloads provided"}), 400
    collection = _get_collection(source)
    
    results = []
    
    def process_payload(payload):
        job_name = _extract_job_name(source, payload)
        job_id = payload.get("id")
        
        if job_name in MIGRATED_FORM_TYPES:
            existing = (
                fs_db.collection(collection)
                .where(filter=FieldFilter("job_id", "==", job_id))
                .limit(1)
                .get()
            )
            if existing:
                doc_id = existing[0].id
                update_firestore_status(
                    doc_id=doc_id,
                    status="new",
                    collection=collection,
                    fields={
                        "payload": payload,
                        "job_name": job_name,
                        "run_retries": 0,
                        "updated_at": firestore.SERVER_TIMESTAMP,
                    },
                )
            else:
                doc_id = save_to_firestore(payload, job_name, "new", collection)
            logger.info({"message": "Payload stored", "job_name": job_name, "doc_id": doc_id, "job_id": job_id})
            return {"status": "stored", "job_name": job_name, "doc_id": doc_id, "job_id": job_id}
        else:
            logger.warning({"message": "Job skipped", "job_name": job_name, "job_id": job_id})
            return {"status": "skipped", "job_name": job_name, "job_id": job_id}
    
    # Use ThreadPoolExecutor for concurrent processing of payloads. Iterate through payloads in batches of 30 to avoid overwhelming Firestore with too many concurrent writes.
    with ThreadPoolExecutor(max_workers=30) as executor:
        futures = [executor.submit(process_payload, payload) for payload in payloads]
        for future in concurrent.futures.as_completed(futures):
            results.append(future.result())
                
    return jsonify({"message": "Bulk save completed", "Payload Count": len(results), "results": results}), 200
        

# -------------------------------------
# PROCESS JOBS (NEW)
# -------------------------------------
@app.route("/process-jobs/<source>", methods=["GET"])
def process_jobs(source: str):
    """Process all 'new' jobs from Firestore"""
    collection = _get_collection(source)
    docs = (
        fs_db.collection(collection)
        .where(filter=FieldFilter("status", "==", "new"))
        .limit(10)
        .get()
    )

    if not docs:
        return jsonify({"message": "No new jobs found"}), 200
    
    # Update to 'Processing'
    for d in docs:
        update_firestore_status(
            doc_id=d.id, collection=collection, status="processing"
        )
        
    results = [
        _process_and_update_job(d.id, d.to_dict(), collection, is_retry=False)
        for d in docs
    ]
    return jsonify({"processed": len(results), "results": results}), 200


# -------------------------------------
# RETRY FAILED JOBS
# -------------------------------------
@app.route("/retry-job/<source>", defaults={"job_id": None}, methods=["GET", "POST"])
@app.route("/retry-job/<source>/<job_id>", methods=["GET"])
def retry_job(source: str, job_id: str):
    """Retry jobs (single, bulk, or auto-retry failed)."""
    collection = _get_collection(source)
    job_ids = []

    try:
        if request.method == "POST":
            data = request.get_json(silent=True) or {}
            job_ids = data.get("ids", [])

        # 1: Single job retry
        if job_id:
            docs = (
                fs_db.collection(collection)
                .where(filter=FieldFilter("job_id", "==", job_id))
                .limit(1)
                .get()
            )

        # 2: Bulk retry by list of IDs
        elif job_ids:
            docs = []
            for jid in job_ids:
                res = (
                    fs_db.collection(collection)
                    .where(filter=FieldFilter("job_id", "==", jid))
                    .limit(1)
                    .get()
                )
                if res:
                    docs.append(res[0])

        # 3: Auto-retry failed jobs
        else:
            docs = (
                fs_db.collection(collection)
                .where(filter=FieldFilter("status", "==", "failed"))
                .where(filter=FieldFilter("run_retries", "<", MAX_RETRIES))
                .limit(10)
                .get()
            )
            if not docs:
                return jsonify({"error": "No jobs found to Auto retry"}), 200

        if not docs:
            return jsonify({"error": "No jobs found to retry"}), 404

        results = []
        for d in docs:
            result = _process_and_update_job(
                d.id, d.to_dict(), collection, is_retry=True
            )
            results.append({"job_id": d.id, "status": "retried", "result": result})

        return jsonify({"Retried": len(results), "results": results}), 200

    except Exception as e:
        logger.exception("Retry job failed")
        return jsonify({"error": str(e)}), 500


# -------------------------------------
# JOB STATUS SUMMARY
# -------------------------------------
@app.route("/status-count/<source>", methods=["GET"])
def status_count(source: str):
    """Summarize jobs by status"""
    collection = _get_collection(source)
    statuses = ["new", "processing", "failed", "completed"]
    summary = {}
    try:
        for status in statuses:
            query = (
                fs_db.collection(collection)
                .where(filter=FieldFilter("status", "==", status))
            )

            result = query.count().get(retry=Retry(deadline=120))
            summary[status] = result[0][0].value

        return jsonify(summary), 200
    except Exception as e:
        logger.error(
            {"message": "Failed to retrieve job statuses", "error": str(e)}
        )
        return jsonify({"error": str(e)}), 500
 


# -----------------------------
# GET PAYLOAD(S)
# -----------------------------
@app.route("/get-payload/<source>", defaults={"job_id": None}, methods=["GET", "POST"])
@app.route("/get-payload/<source>/<job_id>", methods=["GET"])
def get_payload(source: str, job_id: str):
    """Retrieve payloads by source, optionally filtered by job_id or list of job_ids"""
    collection = _get_collection(source)

    try:
        # Handle optional limit (e.g. ?limit=20)
        limit = request.args.get("limit")
        limit = int(limit) if limit and limit.isdigit() else None

        # Handle bulk POST
        job_ids = []
        if request.method == "POST":
            data = request.get_json(silent=True) or {}
            job_ids = data.get("ids", [])

        if job_id:
            # Fetch single job by job_id
            docs = (
                fs_db.collection(collection)
                .where(filter=FieldFilter("job_id", "==", job_id))
                .get()
            )

        elif job_ids:
            # Bulk fetch up to 10 IDs using Firestore "in" filter (limit imposed by Firestore)
            chunk = job_ids[:10]
            docs = (
                fs_db.collection(collection)
                .where(filter=FieldFilter("job_id", "in", chunk))
                .get()
            )

        else:
            # Fetch all or limited payloads, ordered by created_at descending
            query = fs_db.collection(collection).order_by(
                "created_at", direction=firestore.Query.DESCENDING
            )
            if limit:
                query = query.limit(limit)
            docs = query.get()

        # --- RESPONSE ---
        if not docs:
            return jsonify({"message": "No records found"}), 404

        records = [{"id": doc.id, "data": doc.to_dict()} for doc in docs]
        return jsonify(records), 200

    except Exception as e:
        logger.error({"message": "Fetch error", "error": str(e)})
        return jsonify({"error": "Failed to fetch", "details": str(e)}), 500


# -----------------------------
# FAILED JOBS LISTING
# -----------------------------
@app.route("/failed-jobs/<source>", methods=["GET"])
def get_failed_jobs(source: str):
    """Get all failed jobs (summary, without full payloads)"""
    collection = _get_collection(source)
    
    start_date = request.args.get("start_date", "2025-01-01")
    start_date = datetime.strptime(start_date, "%Y-%m-%d")
    
    # print(f"Start Date: {str(start_date)}")
    
    end_date = request.args.get("end_date")
    end_date = datetime.strptime(end_date, "%Y-%m-%d") if end_date else datetime.now(timezone.utc)
    
    # print(f"End Date: {str(end_date)}")
        
    job_name = request.args.get("job_name")
    job_names = [job_name] if job_name else list(job_mapping.keys())
    
    # print(f"Job Names: {str(job_names)}")
    
    docs = (
        fs_db.collection(collection)
        .where(filter=FieldFilter("status", "==", "failed"))
        .where(filter=FieldFilter("created_at", ">=", start_date))
        .where(filter=FieldFilter("created_at", "<=", end_date))
        .where(filter=FieldFilter("job_name", "in", job_names))
        .get()
    )

    jobs = [
        {
            "job_id": d.to_dict().get("job_id"),
            "job_name": d.to_dict().get("job_name"),
            "run_retries": d.to_dict().get("run_retries"),
            "created_at": d.to_dict().get("created_at"),
            "last_retried_at": d.to_dict().get("last_retried_at"),
            "error": d.to_dict().get("error"),
            "payload": d.to_dict().get("payload"),
        }
        for d in docs
    ]
    return jsonify({"failed_count": len(jobs), "jobs": jobs}), 200

# -------------------------------------
# UPDATE PAYLOAD DETAILS
# -------------------------------------
@app.route("/update-payloads/<source>", methods=["POST"])
def update_payloads(source: str):
    """Bulk update the payload details e.g. Status, Number of Retries e.t.c"""

    collection = _get_collection(source)
    data: dict = request.get_json(silent=True) or {}
    update_status = data.get("status", "new")
    update_run_retries = data.get("run_retries", 0)
    job_ids = data.get("job_ids")

    def chunked(iterable, size=30):
        it = iter(iterable)
        while True:
            chunk = list(itertools.islice(it, size))
            if not chunk:
                break
            yield chunk
    
    def fetch_chunk(id_chunk):
        return list(
            fs_db.collection(collection).where(filter=FieldFilter("job_id", "in", id_chunk)).stream()
        )

    try:
        results = []
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = [
                executor.submit(
                    fetch_chunk,
                    chunk
                )
                for chunk in chunked(job_ids, 30)
            ]
            for f in futures:
                results.extend(f.result())

        batch_size = 500
        for i in range(0, len(results), batch_size):
            batch = fs_db.batch()
            chunk = results[i:i+batch_size]
            for doc in chunk:
                logger.info({
                    "message": f"Parsing document {str(doc.id)}"
                })
                doc_ref = fs_db.collection(collection).document(doc.id)
                update_data = {
                    "status": update_status,
                    "updated_at": str(datetime.now(timezone.utc)),
                    "run_retries": int(update_run_retries)
                }
                batch.update(doc_ref, update_data)
            batch.commit()
        
        return jsonify({"message": "Update completed"}), 200
    except Exception as e:
        return jsonify({"error": "Failed to update records", "details": str(e)}), 500

# -------------------------------------
# INTERNAL HELPERS
# -------------------------------------
def _get_collection(source: str):
    if source.lower() in ["commcare", "cc"]:
        return "commcare_payloads"
    elif source.lower() in ["postgres", "pg", "postgresql"]:
        return "postgres_payloads"
    else:
        raise ValueError(f"Invalid source: {source}")


def _extract_job_name(source: str, payload: dict):
    if source.lower() in ["commcare", "cc"]:
        job_name = payload.get("form", {}).get("@name")
        if (
            job_name == "Followup"
            and payload.get("form", {}).get("survey_type", "") == "Attendance Light"
        ):
            job_name = "Attendance Light - Current Module"
        return job_name
    elif source.lower() in ["postgres", "pg", "postgresql"]:
        return payload.get("jobType")
    return None


def _process_and_update_job(doc_id: str, data: dict, collection: str, is_retry=False):
    """Core job processing + Firestore update"""
    db = SessionLocal()
    try:
        job_name = data.get("job_name")
        job_orchestrator = job_mapping.get(job_name)

        if not job_orchestrator:
            update_firestore_status(
                doc_id=doc_id,
                collection=collection,
                status="failed",
                fields={"error": f"Unhandled job type '{job_name}'"},
            )
            return {
                "job_id": data.get("job_id"),
                "status": "failed",
                "error": "Job not handled",
            }

        result = job_orchestrator(db).process_data(data.get("payload"), SYSTEM_ID)

        fields = {
            "record_id": str(result.id),
            "error": None,
            "updated_at": firestore.SERVER_TIMESTAMP,
        }

        if is_retry:
            fields["run_retries"] = data.get("run_retries", 0) + 1
            fields["last_retried_at"] = firestore.SERVER_TIMESTAMP

        update_firestore_status(
            doc_id=doc_id, collection=collection, status="completed", fields=fields
        )

        return {
            "job_id": data.get("job_id"),
            "job_type": data.get("job_name"),
            "status": "completed",
            "record_id": str(result.id),
            "run_retries": fields.get("run_retries", data.get("run_retries", 0)),
        }

    except Exception as e:
        retries = (
            data.get("run_retries", 0) + 1 if is_retry else data.get("run_retries", 0)
        )
        update_firestore_status(
            doc_id=doc_id,
            collection=collection,
            status="failed",
            fields={
                "error": str(e),
                "run_retries": retries,
                "last_retried_at": firestore.SERVER_TIMESTAMP if is_retry else None,
            },
        )
        return {
            "job_id": data.get("job_id"),
            "job_type": data.get("job_name"),
            "status": "failed",
            "error": str(e),
            "run_retries": retries,
        }
    finally:
        db.close()

# -------------------------------------
# MAIN ENTRY
# -------------------------------------
if __name__ == "__main__":
    main()
    print("Flask app running on port 8080...")
    app.run(host="0.0.0.0", port=8080, debug=True)
