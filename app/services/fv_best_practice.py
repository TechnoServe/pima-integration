from sqlalchemy.orm import Session
from models import FVBestPractice
from schemas import FVBestPracticeCreate
from core import logger


class FVBestPracticeService:
    """Handles database operations for fv best practices"""

    def __init__(self, db: Session):
        self.db = db

    def upsert(self, data: FVBestPracticeCreate, created_by_id: str) -> FVBestPractice:
        """Create and Update fv best practice data"""

        # Look up existing observation
        existing = (
            self.db.query(FVBestPractice)
            .filter(
                FVBestPractice.submission_id == data.submission_id,
                FVBestPractice.is_deleted == False,
            )
            .first()
        )

        if existing:
            logger.info(
                {
                    "message": f"Updating existing fv best practice for best practice type: '{data.best_practice_type}' with record ID: '{data.submission_id}'"
                }
            )
            return self._update_existing(existing, data, created_by_id)
        else:
            logger.info(
                {"message": f"Creating new fv best practice for best practice type: '{data.best_practice_type}' record: '{data.submission_id}'"}
            )
            return self._create_new(data, created_by_id)

    def _update_existing(
        self, existing: FVBestPractice, data: FVBestPracticeCreate, updated_by_id: str
    ) -> FVBestPractice:
        """Update existing fv best practice with smart merging"""

        # Smart update: don't overwrite existing data with None values
        for field, value in data.model_dump(exclude_unset=True).items():
            if field in ["submission_id", "farm_visit_id"]:
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

    def _create_new(self, data: FVBestPracticeCreate, created_by_id: str) -> FVBestPractice:
        """Create new fv best practice"""

        observation = FVBestPractice(
            **data.model_dump(exclude_unset=True),
            created_by_id=created_by_id,
            last_updated_by_id=created_by_id,
        )

        self.db.add(observation)
        self.db.commit()
        self.db.refresh(observation)
        return observation
