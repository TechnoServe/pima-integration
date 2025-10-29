from sqlalchemy.orm import Session
from models import FarmVisit
from schemas import FarmVisitCreate
from core import logger


class FarmVisitService:
    """Handles database operations for farm visits"""

    def __init__(self, db: Session):
        self.db = db

    def upsert(self, data: FarmVisitCreate, created_by_id: str) -> FarmVisit:
        """Create and Update farm visit data"""

        # Look up existing farm_visit
        existing = (
            self.db.query(FarmVisit)
            .filter(
                FarmVisit.submission_id == data.submission_id,
                FarmVisit.is_deleted == False,
            )
            .first()
        )

        if existing:
            logger.info(
                {
                    "message": f"Updating existing farm visit record: {data.submission_id}"
                }
            )
            return self._update_existing(existing, data, created_by_id)
        else:
            logger.info(
                {"message": f"Creating new farm visit record: {data.submission_id}"}
            )
            return self._create_new(data, created_by_id)

    def _update_existing(
        self, existing: FarmVisit, data: FarmVisitCreate, updated_by_id: str
    ) -> FarmVisit:
        """Update existing farm visit with smart merging"""

        # Smart update: don't overwrite existing data with None values
        for field, value in data.model_dump(exclude_unset=True).items():
            if field in [
                "visited_primary_farmer_id",
                "submission_id",
                "visited_secondary_farmer_id",
                "visited_household_id",
                "training_session_id",
                "visiting_staff_id",
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

    def _create_new(self, data: FarmVisitCreate, created_by_id: str) -> FarmVisit:
        """Create new farm visit"""

        farm_visit = FarmVisit(
            **data.model_dump(exclude_unset=True),
            created_by_id=created_by_id,
            last_updated_by_id=created_by_id,
        )

        # print(f"DATA: {str(data)}")
        # print(f"CREATED BY: {created_by_id}")
        # print(f"FarmVisit Data: {farm_visit.}")

        try:
            self.db.add(farm_visit)
            self.db.commit()
            self.db.refresh(farm_visit)
        except Exception as e:
            logger.error(
                {
                    "message": "DB insert failed",
                    "exception": repr(e),
                    # "traceback": traceback.format_exc()
                }
            )
            raise
        return farm_visit
