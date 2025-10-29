from sqlalchemy.orm import Session
from models import Check
from schemas import CheckCreate
from core import logger


class CheckService:
    """Handles database operations for varieties"""

    def __init__(self, db: Session):
        self.db = db

    def upsert(self, data: CheckCreate, created_by_id: str) -> Check:
        """Create and Update check data"""

        # Look up existing check
        existing = (
            self.db.query(Check)
            .filter(
                Check.submission_id == data.submission_id,
                Check.is_deleted == False,
            )
            .first()
        )

        if existing:
            logger.info(
                {"message": f"Updating existing check record: {data.submission_id}"}
            )
            return self._update_existing(existing, data, created_by_id)
        else:
            logger.info({"message": f"Creating new check record: {data.submission_id}"})
            return self._create_new(data, created_by_id)

    def _update_existing(
        self, existing: Check, data: CheckCreate, updated_by_id: str
    ) -> Check:
        """Update existing check with smart merging"""

        # Smart update: don't overwrite existing data with None values
        for field, value in data.model_dump(exclude_unset=True).items():
            if field in [
                "submission_id",
                "farmer_id",
                "checker_id",
                "observation_id",
                "farm_visit_id",
                "training_session_id",
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

    def _create_new(self, data: CheckCreate, created_by_id: str) -> Check:
        """Create new check"""

        check = Check(
            **data.model_dump(exclude_unset=True),
            created_by_id=created_by_id,
            last_updated_by_id=created_by_id,
        )

        try:
            self.db.add(check)
            self.db.commit()
            self.db.refresh(check)
        except Exception as e:
            logger.error(
                {
                    "message": "DB insert failed",
                    "exception": repr(e),
                }
            )
            raise
        return check
