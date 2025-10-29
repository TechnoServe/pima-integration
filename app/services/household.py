from sqlalchemy.orm import Session
from models import Household
from schemas import HouseholdCreate
from core import logger


class HouseholdService:
    """Handles database operations for households"""

    def __init__(self, db: Session):
        self.db = db

    def upsert(self, data: HouseholdCreate, created_by_id: str) -> Household:
        """Create and Update household data"""

        # Look up existing training session
        existing = (
            self.db.query(Household)
            .filter(Household.tns_id == data.tns_id, Household.is_deleted == False)
            .first()
        )

        if existing:
            logger.info(
                {"message": f"Updating existing household record: {data.tns_id}"}
            )
            return self._update_existing(existing, data, created_by_id)
        else:
            logger.info({"message": f"Creating new household record: {data.tns_id}"})
            return self._create_new(data, created_by_id)

    def _update_existing(
        self, existing: Household, data: HouseholdCreate, updated_by_id: str
    ) -> Household:
        """Update existing training session with smart merging"""

        # Smart update: don't overwrite existing data with None values
        for field, value in data.model_dump(exclude_unset=True).items():
            if field in ["farmer_group_id", "tns_id"]:
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

    def _create_new(self, data: HouseholdCreate, created_by_id: str) -> Household:
        """Create new household"""

        household = Household(
            **data.model_dump(exclude_unset=True),
            created_by_id=created_by_id,
            last_updated_by_id=created_by_id,
        )

        self.db.add(household)
        self.db.commit()
        self.db.refresh(household)
        return household
