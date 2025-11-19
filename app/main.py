import os
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
        else:
            logger.warning(
                {"message": "Job skipped", "job_name": job_name, "job_id": request_id}
            )

    except Exception as e:
        logger.error(
            {"message": "Failed to save payload", "job_id": request_id, "error": str(e)}
        )
        return jsonify({"error": str(e)}), 500

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
        return jsonify({"message": "No new jobs found"}), 404

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
    for status in statuses:
        count = (
            fs_db.collection(collection)
            .where(filter=FieldFilter("status", "==", status))
            .get()
        )
        summary[status] = len(count)

    return jsonify(summary), 200


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
    docs = (
        fs_db.collection(collection)
        .where(filter=FieldFilter("status", "==", "failed"))
        .get()
    )

    jobs = [
        {
            "job_id": d.to_dict().get("job_id"),
            "job_name": d.to_dict().get("job_name"),
            "run_retries": d.to_dict().get("run_retries"),
            "last_retried_at": d.to_dict().get("last_retried_at"),
        }
        for d in docs
    ]
    return jsonify({"failed_count": len(jobs), "jobs": jobs}), 200


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

        db = SessionLocal()
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


# -------------------------------------
# MAIN ENTRY
# -------------------------------------
if __name__ == "__main__":
    main()
    print("Flask app running on port 8080...")
    app.run(host="0.0.0.0", port=8080, debug=True)
