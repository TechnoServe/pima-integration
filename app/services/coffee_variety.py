from sqlalchemy.orm import Session
from models import CoffeeVariety
from schemas import CoffeeVarietyCreate
from core import logger


class CoffeeVarietyService:
    """Handles database operations for varieties"""

    def __init__(self, db: Session):
        self.db = db

    def upsert(self, data: CoffeeVarietyCreate, created_by_id: str) -> CoffeeVariety:
        """Create and Update variety data"""

        # Look up existing variety
        existing = (
            self.db.query(CoffeeVariety)
            .filter(
                CoffeeVariety.submission_id == data.submission_id,
                CoffeeVariety.is_deleted == False,
            )
            .first()
        )

        if existing:
            logger.info(
                {
                    "message": f"Updating existing variety record: {data.submission_id}"
                }
            )
            return self._update_existing(existing, data, created_by_id)
        else:
            logger.info(
                {"message": f"Creating new variety record: {data.submission_id}"}
            )
            return self._create_new(data, created_by_id)

    def _update_existing(
        self, existing: CoffeeVariety, data: CoffeeVarietyCreate, updated_by_id: str
    ) -> CoffeeVariety:
        """Update existing variety with smart merging"""

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

    def _create_new(self, data: CoffeeVarietyCreate, created_by_id: str) -> CoffeeVariety:
        """Create new variety"""

        variety = CoffeeVariety(
            **data.model_dump(exclude_unset=True),
            created_by_id=created_by_id,
            last_updated_by_id=created_by_id,
        )

        # print(f"DATA: {str(data)}")
        # print(f"CREATED BY: {created_by_id}")
        # print(f"CoffeeVariety Data: {variety.}")

        try:
            self.db.add(variety)
            self.db.commit()
            self.db.refresh(variety)
        except Exception as e:
            logger.error(
                {
                    "message": "DB insert failed",
                    "exception": repr(e),
                    # "traceback": traceback.format_exc()
                }
            )
            raise
        return variety
