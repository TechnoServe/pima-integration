from sqlalchemy.orm import Session
from models import Farmer
from schemas import FarmerCreate
from core import logger


class FarmerService:
    """Handles database operations for farmers"""

    def __init__(self, db: Session):
        self.db = db

    def upsert(self, data: FarmerCreate, created_by_id: str) -> Farmer:
        """Update farmer data"""

        # Look up existing training session
        existing = (
            self.db.query(Farmer)
            .filter(
                Farmer.commcare_case_id == data.commcare_case_id,
                Farmer.is_deleted == False,
            )
            .first()
        )

        if existing:
            logger.info({"message": f"Updating existing farmer record: {data.tns_id}"})
            return self._update_existing(existing, data, created_by_id)
        else:
            logger.info({"message": f"Creating new farmer record: {data.tns_id}"})
            return self._create_new(data, created_by_id)

    def _update_existing(
        self, existing: Farmer, data: FarmerCreate, updated_by_id: str
    ) -> Farmer:
        """Update existing training session with smart merging"""

        # Smart update: don't overwrite existing data with None values
        for field, value in data.model_dump(exclude_unset=True).items():
            if field in [
                "farmer_group_id",
                "household_id",
                "commcare_case_id",
                "tns_id",
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

    def _create_new(self, data: FarmerCreate, created_by_id: str) -> Farmer:
        """Create new farmer"""

        farmer = Farmer(
            **data.model_dump(exclude_unset=True),
            created_by_id=created_by_id,
            last_updated_by_id=created_by_id,
        )

        self.db.add(farmer)
        self.db.commit()
        self.db.refresh(farmer)
        return farmer
    
    def deactivate_farmer(self, commcare_case_id: str, updated_by_id: str) -> None:
        """Deactivate a farmer by commcare_case_id"""
        farmer: Farmer = (
            self.db.query(Farmer)
            .filter(Farmer.commcare_case_id == commcare_case_id, Farmer.is_deleted == False)
            .first()
        )

        if farmer:
            farmer.status = "Inactive"
            farmer.status_notes = "Deactivated. Replaced"
            farmer.send_to_commcare = True
            farmer.last_updated_by_id = updated_by_id
            self.db.commit()
            self.db.refresh(farmer)
            logger.info({"message": f"Deactivated farmer: {commcare_case_id}"})
        else:
            logger.info({"message": f"No farmer found to deactivate: {commcare_case_id}"})
