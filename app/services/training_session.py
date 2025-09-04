from sqlalchemy.orm import Session
import datetime
from models.training_session import TrainingSession
from schemas.training_session import TrainingSessionSchema
import uuid

def upsert_training_session(session: Session, schema: TrainingSessionSchema, training_session_type: str) -> TrainingSession:
    """
    Upsert a TrainingSession record using commcare_case_id as unique key.
    """
    existing = (
        session.query(TrainingSession)
        .filter_by(commcare_case_id=schema.commcare_case_id)
        .first()
    )

    if existing:
        updates = schema.model_dump(exclude_unset=True)

        # Fields allowed to update
        
        if training_session_type == "attendance_light_ft":
            UPDATABLE_FIELDS = {
                "trainer_id",
                "date_session_1",
                "male_attendees_session_1",
                "female_attendees_session_1",
                "total_attendees_session_1",
                "location_gps_latitude_session_1",
                "location_gps_longitude_session_1",
                "location_gps_altitude_session_1",
                "send_to_commcare_status",
            }
        elif training_session_type == "attendance_light_aa":
            UPDATABLE_FIELDS = {
                "trainer_id",
                "date_session_2",
                "male_attendees_session_2",
                "female_attendees_session_2",
                "total_attendees_session_2",
                "location_gps_latitude_session_2",
                "location_gps_longitude_session_2",
                "location_gps_altitude_session_2",
                "send_to_commcare_status",
            }
        for field, value in updates.items():
            if field in UPDATABLE_FIELDS and value is not None:
                setattr(existing, field, value)

        existing.updated_at = datetime.datetime.now(datetime.timezone.utc)
        existing.last_updated_by = uuid.UUID("08e72c7a-4194-4e72-b3ec-ae52defa8be3")  # System user
        session.add(existing)
        return existing

    else:
        new_record = TrainingSession(**schema.model_dump(exclude_unset=True))
        new_record.created_at = datetime.datetime.now(datetime.timezone.utc)
        new_record.updated_at = datetime.datetime.now(datetime.timezone.utc)
        new_record.created_by = uuid.UUID("08e72c7a-4194-4e72-b3ec-ae52defa8be3")  # System user
        new_record.last_updated_by = uuid.UUID("08e72c7a-4194-4e72-b3ec-ae52defa8be3")  # System user
        session.add(new_record)
        return new_record
