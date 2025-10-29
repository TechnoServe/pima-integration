from typing import Dict, Any
from schemas import ObservationResultCreate
from models import Observation
from services import ForeignKeyResolver
from core import logger
from pydantic import ValidationError


class ObservationResultTransformer:
    """Transforms CommCare payload to database-ready schema"""

    def __init__(self, resolver: ForeignKeyResolver):
        self.resolver = resolver

    def transform(self, raw_payload: Dict, cleaned_payload: Dict) -> ObservationResultCreate:
        """Transform CommCare payload to ObservationResultCreate schema"""
        try:

            session_data = self._map_observation_result_data(cleaned_payload)
            
            # Resolve IDs
            observation_id = self.resolver.resolve_db_id(
                raw_payload.get("id"),
                Observation.submission_id,
                "Observation",
                Observation
            ).id
            
            return ObservationResultCreate(
                observation_id=observation_id, 
                **session_data
            )

        except ValidationError as e:
            logger.error(
                {"message": "Schema validation failed", "errors": str(e.errors())}
            )
            raise ValueError(f"Schema validation failed: {str(e.errors())}") from e

    def _map_observation_result_data(self, payload: Dict) -> Dict[str, Any]:
        """Map observation result data"""
        return {
            "submission_id": payload.get("submission_id"),
            "criterion": payload.get("criterion"),
            "question_key": payload.get("question_key"),
            "result_text": payload.get("result_text", None),
            "result_numeric": payload.get("result_numeric"),
            "result_boolean": payload.get("result_boolean"),
            "result_url": payload.get("result_url"),
        }
