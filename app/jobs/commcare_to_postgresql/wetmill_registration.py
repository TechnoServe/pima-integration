from core import logger
from sqlalchemy.orm import Session 
from models import Wetmill
from transformations import WetmillTransformer
from services import ForeignKeyResolver, WetmillService


class WetmillRegistrationOrchestrator:
    def __init__(self, db: Session):
        self.db = db
        self.resolver = ForeignKeyResolver(self.db)
        self.wetmill_registration_transformer = WetmillTransformer(self.db)
        self.wetmill_registration_service = WetmillService(self.db)

    def process_data(self, raw_payload: dict, created_by_id: str):
        """Complete workflow for processing wetmill registration"""

        # 1. Process wetmill registration
        return self.process_wetmill_registration(raw_payload, created_by_id)

    def process_wetmill_registration(
        self, raw_payload: dict, created_by_id: str
    ) -> Wetmill:
        payload = raw_payload

        # 1. Process Wetmill Visit
        try:
            transformed_data = self.wetmill_registration_transformer.transform(
                payload=payload
            )

            result = self.wetmill_registration_service.upsert(
                data=transformed_data, created_by_id=created_by_id
            )

            logger.info(
                {f"Upserted wetmill registration with record ID: '{result.id}'"}
            )

            return result
        except ValueError as e:
            self.db.rollback()
            logger.error(
                {"message": f"Value error in wetmill registration processing: {str(e)}"}
            )
            raise

        except Exception as e:
            logger.error({f"Error processing wetmill registration: {str(e)}"})
            self.db.rollback()
            raise
