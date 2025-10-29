from sqlalchemy.orm import Session
from services import ForeignKeyResolver, FarmerService, HouseholdService
from transformations import FarmerTransformer, HouseholdTransformer
from models import Farmer, Household
from core import logger
from jobs.commcare_to_postgresql import AttendanceFullOrchestrator


class ParticipantRegistrationAndUpdateOrchestrator:
    """Orchestrates the entire ingestion process"""

    def __init__(self, db: Session):
        self.db = db
        self.resolver = ForeignKeyResolver(db)
        self.farmertransformer = FarmerTransformer(self.resolver)
        self.farmerservice = FarmerService(db)
        self.householdtransformer = HouseholdTransformer(self.resolver)
        self.householdservice = HouseholdService(db)
        self.attendanceorchestrator = AttendanceFullOrchestrator(db)

    def process_data(self, raw_payload: dict, created_by_id: str):
        """Complete workflow for processing farmer registration, update, and deactivation"""
        # 1. Process household data
        self.process_household(raw_payload, created_by_id)

        # 2. Process farmer data
        return self.process_farmer(raw_payload, created_by_id)

    def process_household(self, raw_payload: dict, created_by_id: str) -> Household:
        """Complete workflow for processing household payload"""

        try:
            # Step 1: Parse raw JSON into Pydantic schema
            payload = raw_payload

            # Step 2: Transform payload (includes foreign key resolution)
            transformed_data = self.householdtransformer.transform(payload)

            # Step 3: Upsert to database
            result = self.householdservice.upsert(transformed_data, created_by_id)

            logger.info({f"Upserted household with record ID: '{result.id}'"})

            return result

        except ValueError as e:
            self.db.rollback()
            logger.error({"message": f"Value error in household processing: {str(e)}"})
            raise

        except Exception as e:
            logger.error({f"Error processing household: {str(e)}"})
            self.db.rollback()
            raise

    def process_farmer(self, raw_payload: dict, created_by_id: str) -> Farmer:
        """Complete workflow for processing farmer payload"""

        try:
            # Step 1: Parse raw JSON into Pydantic schema
            payload = raw_payload

            # Step 2: Transform payload (includes foreign key resolution)
            transformed_data = self.farmertransformer.transform(payload)

            # Step 3: Upsert to database
            result = self.farmerservice.upsert(transformed_data, created_by_id)

            logger.info({f"Upserted farmer with record ID: '{result.id}'"})

            # Step 4: Process farmer deactivation
            self._handle_deactivation(payload, created_by_id)

            # Step 5: Process attendance data
            self.attendanceorchestrator.process_attendance(
                payload, Farmer.commcare_case_id, created_by_id
            )

            return result

        except ValueError as e:
            self.db.rollback()
            logger.error({"message": f"Value error in farmer processing: {str(e)}"})
            raise

        except Exception as e:
            logger.error({f"Error processing farmer: {str(e)}"})
            self.db.rollback()
            raise

    def _handle_deactivation(self, payload: dict, created_by_id: str):
        """Deactivate existing farmer if conditions are met"""
        form = payload.get("form", {})
        cond_both_filled = form.get("existing_household.both_filled", {}).get(
            "replaced_member_full", ""
        )
        cond_primary_filled = form.get(
            "existing_household.primary_spot_filled", {}
        ).get("primary_replace_adding", "")
        cond_secondary_filled = form.get(
            "existing_household.secondary_spot_filled", {}
        ).get("secondary_replace_adding", "")

        try:
            if cond_both_filled == "1" or cond_primary_filled == "2":
                old_farmer_id = form.get("existing_household", {}).get(
                    "existing_primary_farmer_id"
                )
                if old_farmer_id:
                    self.farmerservice.deactivate_farmer(old_farmer_id, created_by_id)

            elif cond_both_filled == "2" or cond_secondary_filled == "2":
                old_farmer_id = form.get("existing_household", {}).get(
                    "existing_secondary_farmer_id"
                )
                if old_farmer_id:
                    self.farmerservice.deactivate_farmer(old_farmer_id, created_by_id)

            else:
                logger.info({"message": "Skipping participant deactivation"})

        except ValueError as e:
            self.db.rollback()
            logger.error({"message": f"Value error in farmer deactivation: {str(e)}"})
            raise

        except Exception as e:
            logger.error({f"Error processing farmer deactivation: {str(e)}"})
            self.db.rollback()
            raise
