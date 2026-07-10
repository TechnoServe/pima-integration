from sqlalchemy.orm import Session
from services import ForeignKeyResolver, TrainingSessionService, ImageService
from transformations import TrainingSessionTransformer, ImageTransformer
from models import TrainingSession
from copy import deepcopy
from core import logger
from dataclasses import dataclass

@dataclass
class finalResult:
    id: list

class AttendanceLightOrchestrator:
    """Orchestrates the entire ingestion process"""

    def __init__(self, db: Session):
        self.db = db
        self.resolver = ForeignKeyResolver(db)
        self.transformer = TrainingSessionTransformer(self.resolver)
        self.service = TrainingSessionService(db)
        self.image_transformer = ImageTransformer()
        self.image_service = ImageService(self.db)

    def process_data(self, raw_payload: dict, created_by_id: str):

        # Process training session data
        return self.process_training_session_preliminary(raw_payload, created_by_id)

    def process_training_session(
        self, raw_payload: dict, created_by_id: str
    ) -> TrainingSession:
        """Complete workflow for processing training session payload"""

        try:
            # Step 1: Parse raw JSON into Pydantic schema
            payload = raw_payload

            # Step 2: Transform payload (includes foreign key resolution)
            transformed_data = self.transformer.transform(payload)

            # Step 3: Upsert to database
            result = self.service.upsert(transformed_data, created_by_id)

            logger.info({f"Upserted training session with record ID: '{result.id}'"})
            
            # Step 4: Upsert associated images if any
            image_url = (
                payload.get("attachments", {})
                .get(payload.get("form", {}).get("photo", ""), {})
                .get("url", "")
            )

            if image_url:
                self.process_image(
                    image_url=image_url,
                    payload=payload,
                    image_reference_obj=result,
                    created_by_id=created_by_id,
                )
            return result

        except ValueError as e:
            self.db.rollback()
            logger.error(
                {"message": f"Value error in training session processing: {str(e)}"}
            )
            raise

        except Exception as e:
            logger.error({f"Error processing training session: {str(e)}"})
            self.db.rollback()
            raise
            
    def process_image(
        self,
        image_url: str,
        payload: dict,
        image_reference_obj: object,
        created_by_id: str,
    ):
        """Placeholder for image processing logic"""

        try:
            if image_url:
                image_data = self.image_transformer.transform(
                    payload=payload,
                    image_url=image_url,
                    image_reference_obj=image_reference_obj,
                    image_description="Attendance",
                )

                image_result = self.image_service.upsert(image_data, created_by_id)

                logger.info(
                    {
                        f"Upserted image with record ID: '{image_result.id}' for training session ID: '{image_reference_obj.id}'"
                    }
                )

                return image_result
        except ValueError as e:
            self.db.rollback()
            logger.error({"message": f"Value error in image processing: {str(e)}"})
            raise
        except Exception as e:
            self.db.rollback()
            logger.error({"message": f"Unexpected error in image processing: {str(e)}"})
            raise
        
    def process_training_session_preliminary(self, raw_payload: dict, created_by_id: str):
        """Check if the trainins session type is for WIL or not"""
        
        payload = raw_payload
        
        survey_detail = payload.get("form", {}).get("survey_detail", "")
        
        if survey_detail == "Women In Leadership - Attendance":
            logger.info({"message": "Training session is for WIL"})
            
            # 1. Split Training Sessions from mapping
            wil_modules = payload.get("form", {}).get("training_topic", "").split(" ")
            wil_groups = payload.get("form", {}).get("focal_farmer_groups", "").split(" ")
            results = []
            for group in wil_groups:
                # 1. Create a new payload for each WIL group
                new_payload = deepcopy(payload)
                new_payload["form"]["focal_farmer_groups"] = group
                
                for module in wil_modules:
                    # 2. Create a new payload for each WIL session
                    new_payload["form"]["training_topic"] = module
                    
                    # 3. Process each WIL session
                    results.append(self.process_training_session(new_payload, created_by_id))
            final_result = finalResult(id=results)
            return final_result
        else:
            logger.info({"message": "Training session is not for WIL"})
            return self.process_training_session(payload, created_by_id)

        
