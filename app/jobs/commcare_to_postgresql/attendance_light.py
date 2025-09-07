from core.postgresql_util import SessionLocal
from transformations.training_session import attendance_light_map
from services.training_session import upsert_training_session
from core.logging_util import logger
from models.training_session import TrainingSession

def run_attendance_light_ft_job(payload: dict):
    """
    Process an attendance_light FT form payload and upsert into training_sessions.
    """
    session = SessionLocal()
    try:
        # 1. Map JSON → Schema
        schema = attendance_light_map(payload)

        # 3. Upsert
        upsert_training_session(session, schema)
        
        session.commit()
        
        record_id = session.query(TrainingSession).filter_by(commcare_case_id=schema.commcare_case_id).first().id
        
        # 5. Logging
        
        logger.info({
            "status": "success",
            "message": f"Upserted training session for case_id {schema.commcare_case_id}",
            "request_id": payload.get("id", ""),
            "record_id": record_id
        })
        
    except Exception as e:
        session.rollback()
        logger.error({
            "status": "error",
            "message": str(e),
            "request_id": payload.get("id", "")
        })
        raise
    finally:
        session.close()
        
