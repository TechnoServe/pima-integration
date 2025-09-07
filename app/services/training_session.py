from sqlalchemy.orm import Session
import datetime
from models.training_session import TrainingSession
from models.staff import Staff
from schemas.training_session import TrainingSessionSchema
from services.resolvers import resolve_id
import uuid
from dotenv import load_dotenv
import os
load_dotenv

SYSTEM_ID = os.getenv('SYSTEM_ID')

def upsert_training_session(session: Session, schema: TrainingSessionSchema) -> TrainingSession:
    """
    Upsert a TrainingSession record using commcare_case_id as unique key.
    """
    
    # Check for existing record
    existing = (
        session.query(TrainingSession)
        .filter_by(commcare_case_id=schema.commcare_case_id)
        .first()
    )

    # Update Exisiting Record
    if existing:
        updates = schema.model_dump(exclude_unset=True)
        for field, value in updates.items():
            setattr(existing, field, value)

        existing.trainer_id = resolve_id(session, schema.commcare_case_id, Staff)
        existing.last_updated_by = uuid.UUID(SYSTEM_ID)  # System user
        session.add(existing)
        return existing

    # Create New Record
    else:
        new_record = TrainingSession(**schema.model_dump(exclude_unset=True))
        new_record.created_by = uuid.UUID(SYSTEM_ID)  # System user
        new_record.last_updated_by = uuid.UUID(SYSTEM_ID)  # System user
        session.add(new_record)
        return new_record