from models import Wetmill
from schemas import WetmillCreate
from core import logger
from sqlalchemy.orm import Session

class WetmillService:
    """Handles database operations for wetmills"""

    def __init__(self, db: Session):
        self.db = db

    def upsert(self, data: WetmillCreate, created_by_id: str) -> Wetmill:
        """Create and Update wetmill data"""

        # Look up existing wetmill
        existing = (
            self.db.query(Wetmill)
            .filter(
                Wetmill.commcare_case_id == data.commcare_case_id,
                Wetmill.is_deleted == False,
            )
            .first()
        )

        if existing:
            logger.info(
                {
                    "message": f"Updating existing wetmill record: {data.commcare_case_id}"
                }
            )
            return self._update_existing(existing, data, created_by_id)
        else:
            logger.info(
                {"message": f"Creating new wetmill record: {data.commcare_case_id}"}
            )
            return self._create_new(data, created_by_id)

    def _update_existing(
        self, existing: Wetmill, data: WetmillCreate, updated_by_id: str
    ) -> Wetmill:
        """Update existing wetmill with smart merging"""

        # Smart update: don't overwrite existing data with None values
        for field, value in data.model_dump(exclude_unset=True).items():
            if field in ["commcare_case_id", "user_id"]:
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

    def _create_new(self, data: WetmillCreate, created_by_id: str) -> Wetmill:
        """Create new wetmill"""

        wetmill = Wetmill(
            **data.model_dump(exclude_unset=True),
            created_by_id=created_by_id,
            last_updated_by_id=created_by_id,
        )

        try:
            self.db.add(wetmill)
            self.db.commit()
            self.db.refresh(wetmill)
        except Exception as e:
            logger.error({
                "message": "DB insert failed",
                "exception": repr(e),
                # "traceback": traceback.format_exc()
            })
            raise
        return wetmill
