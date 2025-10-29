from sqlalchemy.orm import Session
from models import FVBestPracticeAnswer
from schemas import FVBestPracticeAnswerCreate
from core import logger


class FVBestPracticeAnswerService:
    """Handles database operations for fv best practice answers"""

    def __init__(self, db: Session):
        self.db = db

    def upsert(
        self, data: FVBestPracticeAnswerCreate, created_by_id: str
    ) -> FVBestPracticeAnswer:
        """Create and Update fv best practice answer data"""

        # Look up existing observation
        existing = (
            self.db.query(FVBestPracticeAnswer)
            .filter(
                FVBestPracticeAnswer.submission_id == data.submission_id,
                FVBestPracticeAnswer.is_deleted == False,
            )
            .first()
        )

        if existing:
            logger.info(
                {
                    "message": f"Updating existing fv best practice answer for question key: '{data.question_key}' with record ID: '{data.submission_id}'"
                }
            )
            return self._update_existing(existing, data, created_by_id)
        else:
            logger.info(
                {
                    "message": f"Creating new fv best practice answer for question key: '{data.question_key}' record: '{data.submission_id}'"
                }
            )
            return self._create_new(data, created_by_id)

    def _update_existing(
        self,
        existing: FVBestPracticeAnswer,
        data: FVBestPracticeAnswerCreate,
        updated_by_id: str,
    ) -> FVBestPracticeAnswer:
        """Update existing fv best practice answer with smart merging"""

        # Smart update: don't overwrite existing data with None values
        for field, value in data.model_dump(exclude_unset=True).items():
            if field in ["submission_id", "fv_best_practice_id"]:
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

    def _create_new(
        self, data: FVBestPracticeAnswerCreate, created_by_id: str
    ) -> FVBestPracticeAnswer:
        """Create new fv best practice answer"""

        observation = FVBestPracticeAnswer(
            **data.model_dump(exclude_unset=True),
            created_by_id=created_by_id,
            last_updated_by_id=created_by_id,
        )

        self.db.add(observation)
        self.db.commit()
        self.db.refresh(observation)
        return observation
