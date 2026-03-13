"""Farmer Group Services"""
from sqlalchemy.orm import Session
from models import FarmerGroup
from schemas import FarmerGroupUpdate
from core import logger

class FarmerGroupService:
    """Handles database operations for farmer groups"""

    def __init__(self, db: Session):
        self.db = db

    def update(self, data: FarmerGroupUpdate, updated_by_id: str) -> FarmerGroup:
        """Update farmer group data"""
        existing = (
            self.db.query(FarmerGroup)
            .filter(
                FarmerGroup.commcare_case_id == data.commcare_case_id,
                FarmerGroup.is_deleted == False,
            )
            .first()
        )

        if not existing:
            logger.warning(f"No existing farmer group found with case ID: {data.commcare_case_id}")
            raise ValueError(f"Farmer group with case ID {data.commcare_case_id} not found")

        # Check if any meaningful fields are being updated
        SKIPPED_FIELDS = {"commcare_case_id"}
        TO_UPDATE = {"focal_farmer_id", "assistant_focal_farmer_id"}

        fields_to_update = {
            field: value
            for field, value in data.model_dump(exclude_unset=True).items()
            if field in TO_UPDATE
        }

        if not fields_to_update:
            logger.info(f"No fields to update for farmer group: {data.commcare_case_id}")
            return existing

        logger.info(f"Updating farmer group record: {data.commcare_case_id}")

        for field, value in fields_to_update.items():
            setattr(existing, field, value)

        existing.last_updated_by_id = updated_by_id
        existing.send_to_commcare = True  # Mark for sync back to CommCare
        existing.send_to_commcare_status = 'Pending'
        self.db.commit()
        self.db.refresh(existing)
        return existing