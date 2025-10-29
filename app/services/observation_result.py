from sqlalchemy.orm import Session
from models import ObservationResult
from schemas import ObservationResultCreate
from core import logger


class ObservationResultService:
    """Handles database operations for observation results"""

    def __init__(self, db: Session):
        self.db = db

    def upsert(self, data: ObservationResultCreate, created_by_id: str) -> ObservationResult:
        """Create and Update observation result data"""

        # Look up existing observation
        existing = (
            self.db.query(ObservationResult)
            .filter(
                ObservationResult.submission_id == data.submission_id,
                ObservationResult.is_deleted == False,
            )
            .first()
        )

        if existing:
            logger.info(
                {
                    "message": f"Updating existing observation result for criterion: '{data.criterion}' with record ID: '{data.submission_id}'"
                }
            )
            return self._update_existing(existing, data, created_by_id)
        else:
            logger.info(
                {"message": f"Creating new observation result for criterion: '{data.criterion}' record: '{data.submission_id}'"}
            )
            return self._create_new(data, created_by_id)

    def _update_existing(
        self, existing: ObservationResult, data: ObservationResultCreate, updated_by_id: str
    ) -> ObservationResult:
        """Update existing observation result with smart merging"""

        # Smart update: don't overwrite existing data with None values
        for field, value in data.model_dump(exclude_unset=True).items():
            if field in ["submission_id"]:
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

    def _create_new(self, data: ObservationResultCreate, created_by_id: str) -> ObservationResult:
        """Create new observation result"""

        observation = ObservationResult(
            **data.model_dump(exclude_unset=True),
            created_by_id=created_by_id,
            last_updated_by_id=created_by_id,
        )

        self.db.add(observation)
        self.db.commit()
        self.db.refresh(observation)
        return observation
