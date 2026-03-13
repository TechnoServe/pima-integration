"""Holds the class to orchestrate attendance full forms from CommCare to PostgreSQL"""

from sqlalchemy.orm import Session
from services import ForeignKeyResolver, AttendanceService, FarmerGroupService
from transformations import AttendanceTransformer, FarmerGroupTransformer
from models import Farmer, FarmerGroup
from core import logger
from jobs.commcare_to_postgresql.attendance_light import AttendanceLightOrchestrator
from dataclasses import dataclass


@dataclass
class finalResult:
    id: list


class AttendanceFullOrchestrator:
    """Orchestrates the entire ingestion process"""

    def __init__(self, db: Session):
        self.db = db
        self.resolver = ForeignKeyResolver(db)
        self.transformer = AttendanceTransformer(self.resolver)
        self.service = AttendanceService(db)
        self.farmergrouptransformer = FarmerGroupTransformer(self.resolver)
        self.farmergroupservice = FarmerGroupService(db)
        self.trainingsessionorchestrator = AttendanceLightOrchestrator(db)

    def process_data(self, raw_payload: dict, created_by_id: str):

        # 1. Process training session data first
        self.trainingsessionorchestrator.process_training_session(
            raw_payload=raw_payload, created_by_id=created_by_id
        )
        # 2. Process training group (FF & AFF)
        self.process_farmer_group(
            raw_payload=raw_payload, created_by_id=created_by_id
        )
        # 3. Process attendance data
        return self.process_attendance(
            payload=raw_payload,
            id_column=Farmer.commcare_case_id,
            created_by_id=created_by_id,
        )

    def process_attendance(
        self, payload: dict, id_column, created_by_id: str
    ) -> object:
        """Complete workflow for processing attendance payload"""
        FARMER_ID = {
            "New Farmer New Household": (payload.get("form", {}).get("subcase_0") or {}).get("case", {}).get("@case_id", ""),
            "New Farmer Existing Household": (payload.get("form", {}).get("subcase_0") or {}).get("case", {}).get("@case_id", ""),
            "Existing Farmer Change in FFG": payload.get("form", {}).get("existing_farmer_change_in_ffg", {}).get("old_farmer_id"),
            "Attendance Full - Current Module": payload.get("form", {}).get("present_participants", "")
        }
        try:
            farmer_external_ids = FARMER_ID.get((payload.get("form", {}).get("survey_detail", "Attendance Full - Current Module")),"").split()
            print(f"Farmer IDs: {str(farmer_external_ids)}")
            results = []
            if farmer_external_ids:
                for farmer_external_id in farmer_external_ids:
                    transformed_data = self.transformer.transform(
                        payload, farmer_external_id, id_column
                    )
                    result = self.service.upsert(transformed_data, created_by_id)
                    results.append(result.id)

                    logger.info(
                        {
                            "message": f"Upserted attendance with record ID: '{result.id}'"
                        }
                    )

            final_result = finalResult(id=results)
            return final_result

        except ValueError as e:
            self.db.rollback()
            logger.error({"message": f"Value error in attendance processing: {str(e)}"})
            raise
        except Exception as e:
            self.db.rollback()
            logger.error({"message": f"Unexpected error: {str(e)}"})
            raise
        
    def process_farmer_group(self, raw_payload: dict, created_by_id: str) -> FarmerGroup:
        try:
            # Step 1: Parse raw JSON into Pydantic schema
            payload = raw_payload

            # Step 2: Transform payload (includes foreign key resolution)
            transformed_data = self.farmergrouptransformer.transform(payload)

            # Step 3: Upsert to database
            result = self.farmergroupservice.update(transformed_data, created_by_id)

            logger.info({f"Upserted farmer group with record ID: '{result.id}'"})

            return result

        except ValueError as e:
            self.db.rollback()
            logger.error({"message": f"Value error in farmer group processing: {str(e)}"})
            raise

        except Exception as e:
            logger.error({f"Error processing farmer group: {str(e)}"})
            self.db.rollback()
            raise
