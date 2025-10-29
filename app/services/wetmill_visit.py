from models import WetmillVisit
from schemas import WetmillVisitCreate
from core import logger
from sqlalchemy.orm import Session

class WetmillVisitService:
    """Handles database operations for wetmill visits"""

    def __init__(self, db: Session):
        self.db = db

    def upsert(self, data: WetmillVisitCreate, created_by_id: str) -> WetmillVisit:
        """Create and Update wetmill visit data"""

        # Look up existing wetmill visit
        existing = (
            self.db.query(WetmillVisit)
            .filter(
                WetmillVisit.submission_id == data.submission_id,
                WetmillVisit.is_deleted == False,
            )
            .first()
        )

        if existing:
            logger.info(
                {
                    "message": f"Updating existing wetmill visit record: {data.submission_id}"
                }
            )
            return self._update_existing(existing, data, created_by_id)
        else:
            logger.info(
                {"message": f"Creating new wetmill visit record: {data.submission_id}"}
            )
            return self._create_new(data, created_by_id)

    def _update_existing(
        self, existing: WetmillVisit, data: WetmillVisitCreate, updated_by_id: str
    ) -> WetmillVisit:
        """Update existing wetmill visit with smart merging"""

        # Smart update: don't overwrite existing data with None values
        for field, value in data.model_dump(exclude_unset=True).items():
            if field in ["submission_id", "user_id"]:
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

    def _create_new(self, data: WetmillVisitCreate, created_by_id: str) -> WetmillVisit:
        """Create new wetmill visit"""

        wetmill_visit = WetmillVisit(
            **data.model_dump(exclude_unset=True),
            created_by_id=created_by_id,
            last_updated_by_id=created_by_id,
        )

        try:
            self.db.add(wetmill_visit)
            self.db.commit()
            self.db.refresh(wetmill_visit)
        except Exception as e:
            logger.error({
                "message": "DB insert failed",
                "exception": repr(e),
                # "traceback": traceback.format_exc()
            })
            raise
        return wetmill_visit
