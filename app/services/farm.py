from sqlalchemy.orm import Session
from models import Farm
from schemas import FarmCreate
from core import logger


class FarmService:
    """Handles database operations for farms"""

    def __init__(self, db: Session):
        self.db = db

    def upsert(self, data: FarmCreate, created_by_id: str) -> Farm:
        """Create and Update farm data"""

        # Look up existing farm
        existing = (
            self.db.query(Farm)
            .filter(
                Farm.submission_id == data.submission_id,
                Farm.is_deleted == False,
            )
            .first()
        )

        if existing:
            logger.info(
                {
                    "message": f"Updating existing farm record: {data.submission_id}"
                }
            )
            return self._update_existing(existing, data, created_by_id)
        else:
            logger.info(
                {"message": f"Creating new farm record: {data.submission_id}"}
            )
            return self._create_new(data, created_by_id)

    def _update_existing(
        self, existing: Farm, data: FarmCreate, updated_by_id: str
    ) -> Farm:
        """Update existing farm with smart merging"""

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

    def _create_new(self, data: FarmCreate, created_by_id: str) -> Farm:
        """Create new farm"""

        farm = Farm(
            **data.model_dump(exclude_unset=True),
            created_by_id=created_by_id,
            last_updated_by_id=created_by_id,
        )

        # print(f"DATA: {str(data)}")
        # print(f"CREATED BY: {created_by_id}")
        # print(f"Farm Data: {farm.}")

        try:
            self.db.add(farm)
            self.db.commit()
            self.db.refresh(farm)
        except Exception as e:
            logger.error(
                {
                    "message": "DB insert failed",
                    "exception": repr(e),
                    # "traceback": traceback.format_exc()
                }
            )
            raise
        return farm
