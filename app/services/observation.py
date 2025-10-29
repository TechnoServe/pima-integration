from sqlalchemy.orm import Session
from models import Observation
from schemas import ObservationCreate
from core import logger


class ObservationService:
    """Handles database operations for observations"""

    def __init__(self, db: Session):
        self.db = db

    def upsert(self, data: ObservationCreate, created_by_id: str) -> Observation:
        """Create and Update observation data"""

        # Look up existing observation
        existing = (
            self.db.query(Observation)
            .filter(
                Observation.submission_id == data.submission_id,
                Observation.is_deleted == False,
            )
            .first()
        )

        if existing:
            logger.info(
                {
                    "message": f"Updating existing observation record: {data.submission_id}"
                }
            )
            return self._update_existing(existing, data, created_by_id)
        else:
            logger.info(
                {"message": f"Creating new observation record: {data.submission_id}"}
            )
            return self._create_new(data, created_by_id)

    def _update_existing(
        self, existing: Observation, data: ObservationCreate, updated_by_id: str
    ) -> Observation:
        """Update existing observation with smart merging"""

        # Smart update: don't overwrite existing data with None values
        for field, value in data.model_dump(exclude_unset=True).items():
            if field in ["farmer_group_id", "submission_id", "observer_id"]:
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

    def _create_new(self, data: ObservationCreate, created_by_id: str) -> Observation:
        """Create new observation"""

        observation = Observation(
            **data.model_dump(exclude_unset=True),
            created_by_id=created_by_id,
            last_updated_by_id=created_by_id,
        )

        try:
            self.db.add(observation)
            self.db.commit()
            self.db.refresh(observation)
        except Exception as e:
            logger.error({
                "message": "DB insert failed",
                "exception": repr(e),
                # "traceback": traceback.format_exc()
            })
            raise
        return observation
