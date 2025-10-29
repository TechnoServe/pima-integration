from sqlalchemy.orm import Session
from models import TrainingSession
from schemas import TrainingSessionCreate
from core import logger


class TrainingSessionService:
    """Handles database operations for training sessions"""

    def __init__(self, db: Session):
        self.db = db

    def upsert(
        self, data: TrainingSessionCreate, updated_by_id: str
    ) -> TrainingSession:
        """Update training session data (strict: must already exist)"""

        # Look up existing training session
        existing = (
            self.db.query(TrainingSession)
            .filter(
                TrainingSession.commcare_case_id == data.commcare_case_id,
                TrainingSession.is_deleted == False,
            )
            .first()
        )

        if not existing:

            logger.error(
                {"message": f"Training session not found: {data.commcare_case_id}"}
            )
            raise ValueError(
                f"Training session not found for case ID: {data.commcare_case_id}"
            )

        logger.info(
            {"message": f"Updating existing training session: {data.commcare_case_id}"}
        )
        return self._update_existing(existing, data, updated_by_id)

    def _update_existing(
        self, existing: TrainingSession, data: TrainingSessionCreate, updated_by_id: str
    ) -> TrainingSession:
        """Update existing training session with smart merging"""

        # Smart update: don't overwrite existing data with None values
        for field, value in data.model_dump(exclude_unset=True).items():
            if field in [
                "trainer_id",
                "module_id",
                "farmer_group_id",
                "commcare_case_id",
            ]:
                # Always update core fields
                setattr(existing, field, value)
            elif value is not None:
                current_value = getattr(existing, field, None)
                if current_value is None or value != current_value:
                    setattr(existing, field, value)

        existing.last_updated_by_id = updated_by_id

        self.db.commit()
        self.db.refresh(existing)
        return existing
