from sqlalchemy.orm import Session
from services import ForeignKeyResolver, TrainingSessionService, ImageService
from transformations import TrainingSessionTransformer, ImageTransformer
from models import TrainingSession
from core import logger


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
        return self.process_training_session(raw_payload, created_by_id)

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
