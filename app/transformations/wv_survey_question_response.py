from typing import Dict, Any
from schemas import WVSurveyQuestionResponseCreate
from models import WVSurveyResponse
from services import ForeignKeyResolver
from core import logger
from pydantic import ValidationError
import datetime
from geoalchemy2.shape import from_shape


class WVSurveyQuestionResponseTransformer:
    """Transforms CommCare payload to database-ready schema"""

    def __init__(self, resolver: ForeignKeyResolver):
        self.resolver = resolver

    def transform(
        self,
        payload: dict,
        survey_type: str,
        section_name: str,
        question_name: str,
        answer,
        submission_id,
    ) -> WVSurveyQuestionResponseCreate:
        """Transform CommCare payload to WVSurveyQuestionResponseCreate schema"""
        try:

            session_data = self._map_wv_survey_question_response_data(
                section_name,
                question_name,
                answer,
                submission_id,
            )

            # Resolve IDs
            survey_response_id = self.resolver.resolve_db_id(
                f"SR-{payload.get("id")}-{survey_type}",
                WVSurveyResponse.submission_id,
                "Survey Response",
                WVSurveyResponse,
            ).id

            return WVSurveyQuestionResponseCreate(
                survey_response_id=survey_response_id, **session_data
            )

        except ValidationError as e:
            logger.error(
                {"message": "Schema validation failed", "errors": str(e.errors())}
            )
            raise ValueError(f"Schema validation failed: {str(e.errors())}") from e

    def _map_wv_survey_question_response_data(
        self,
        section_name: str,
        question_name: str,
        answer,
        submission_id,
    ) -> Dict[str, Any]:
        """Map WV survey question response data"""
        field_type, field_value = self._infer_field_type(answer)

        return {
            "submission_id": submission_id,
            "section_name": section_name,
            "question_name": question_name,
            "field_type": field_type,
            "value_text": field_value if field_type == "text" else None,
            "value_number": field_value if field_type == "number" else None,
            "value_boolean": field_value if field_type == "boolean" else None,
            "value_date": field_value if field_type == "date" else None,
            "value_gps": from_shape(field_value, srid=4326) if field_type == "gps" else None,
        }
    
    def _infer_field_type(self, value):
        """
        Infer the data type of the answer and return (field_type, parsed_value).
        - Booleans: 'TRUE', 'FALSE', '1', '0'
        - Dates: ISO format 'YYYY-MM-DD'
        - Numbers: integers or floats (e.g., '50', '50.0')
        - Fallback to text
        """
        # Handle string inputs
        if isinstance(value, str):
            val = value.strip()
            # Detect booleans
            if val.upper() in ("TRUE", "FALSE"):
                return "boolean", (val.upper() == "TRUE")
            if val in ("1", "0"):
                return "boolean", (val == "1")
            # Detect dates
            try:
                dt = datetime.datetime.strptime(val, "%Y-%m-%d")
                return "date", dt
            except:
                pass
            # Detect numbers
            try:
                num = float(val)
                return "number", num
            except:
                pass
            # Otherwise text
            return "text", val or None
        # Non-strings
        elif isinstance(value, bool):
            return "boolean", value
        elif isinstance(value, (int, float)):
            return "number", float(value)
        # Turn unknown types to text
        return "text", str(value) if value is not None else None
