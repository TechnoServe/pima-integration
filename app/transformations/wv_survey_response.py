from typing import Dict, Any
from schemas import WVSurveyResponseCreate
from models import WetmillVisit
from services import ForeignKeyResolver
from core import logger
from pydantic import ValidationError
import datetime


class WVSurveyResponseTransformer:
    """Transforms CommCare payload to database-ready schema"""

    def __init__(self, resolver: ForeignKeyResolver):
        self.resolver = resolver

    def transform(self, payload: Dict, survey_type: str, content: dict) -> WVSurveyResponseCreate:
        """Transform CommCare payload to WVSurveyResponseCreate schema"""
        try:

            session_data = self._map_wv_survey_response_data(payload, survey_type, content)
            
            # Resolve IDs
            form_visit_id = self.resolver.resolve_db_id(
                f"WV-{payload.get("id")}",
                WetmillVisit.submission_id,
                "Wetmill Visit",
                WetmillVisit
            ).id
            
            return WVSurveyResponseCreate(
                form_visit_id=form_visit_id
                **session_data
            )

        except ValidationError as e:
            logger.error(
                {"message": "Schema validation failed", "errors": str(e.errors())}
            )
            raise ValueError(f"Schema validation failed: {str(e.errors())}") from e

    def _map_wv_survey_response_data(self, payload: Dict, survey_type: str, content: dict) -> Dict[str, Any]:
        """Map observation result data"""
        form_id = payload.get("id")
        date_str = payload.get("form", {}).get("date", "")
        date = datetime.date.strftime(date_str, "%Y-%m-%d")
        return {
            "submission_id": f"SR-{form_id}-{survey_type}",
            "survey_type": survey_type,
            "completed_date": date,
            "general_feedback": content.get("general_feedback"),
        }
