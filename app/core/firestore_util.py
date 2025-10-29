from google.cloud import firestore
from google.api_core import exceptions as api_exceptions
from core import logger


def init_db():
    return firestore.Client()


def save_to_firestore(payload, job_name, status, collection, db=None):
    """Func to save file to firestore"""
    if db is None:
        db = init_db()
    
    doc_ref = db.collection(collection).add(
        {
            "payload": payload,
            "job_name": job_name,
            "job_id": payload.get("id"),
            "status": status,
            "run_retries": 0,
            "last_retried_at": "",
            "created_at": firestore.SERVER_TIMESTAMP,
            "updated_at": firestore.SERVER_TIMESTAMP,
        }
    )

    return doc_ref[1].id


def update_firestore_status(doc_id, status, collection, fields=None, db=None):
    if db is None:
        db = init_db()
    try:
        update_data = {"status": status}
        if fields:
            update_data.update(fields)
        db.collection(collection).document(doc_id).update(update_data)
        logger.info(
            {
                "message": "Successfully updated Firestore document",
                "doc_id": doc_id,
                "status": status,
                # "fields": fields,
            }
        )

        return True
    except (
        api_exceptions.GoogleAPICallError,
        api_exceptions.RetryError,
        api_exceptions.NotFound,
    ) as e:
        logger.error(
            {
                "message": "Failed to update Firestore document. API error:",
                "doc_id": doc_id,
                "status": status,
                "fields": fields,
                "error": str(e),
            }
        )
        raise
    except Exception as e:
        logger.error(
            {
                "message": "Failed to update Firestore document. Unhandled exception:",
                "doc_id": doc_id,
                "status": status,
                "fields": fields,
                "error": str(e),
            }
        )
        raise
