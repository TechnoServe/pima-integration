from typing import Dict, Any
from schemas import AttendanceCreate
from services import ForeignKeyResolver, SkipTransformation
from models import TrainingSession, Farmer
from pydantic import ValidationError
from core import logger


class AttendanceTransformer:
    """Transforms CommCare payload to database-ready schema"""

    def __init__(self, resolver: ForeignKeyResolver):
        self.resolver = resolver

    def transform(
        self, payload: Dict, farmer_external_id, id_column
    ) -> AttendanceCreate:
        """Transform CommCare payload to TrainingSessionCreate schema"""

        try:
            # Resolve foreign keys first
            training_session_id = self.resolver.resolve_db_id(
                payload.get("form", {}).get("training_session"),
                TrainingSession.commcare_case_id,
                "Training Session",
                TrainingSession,
            ).id
            farmer_id = self.resolver.resolve_db_id(
                farmer_external_id, id_column, "Farmer", Farmer
            ).id

            # Handle different form types and map to appropriate session fields
            session_data = self._map_attendance_data(payload, farmer_external_id)

            return AttendanceCreate(
                training_session_id=training_session_id,
                farmer_id=farmer_id,
                **session_data,
            )
        except SkipTransformation as e:
            logger.info(str(e))
            return None
        except ValidationError as e:
            logger.error(
                {"message": "Schema validation failed", "errors": str(e.errors())}
            )
            raise ValueError(f"Schema validation failed: {str(e.errors())}") from e

    def _map_attendance_data(
        self, payload: Dict, farmer_external_id: str
    ) -> Dict[str, Any]:
        """Map session data based on form type"""
        form_name = payload.get("form", {}).get("@name", "")

        if form_name in ["Attendance Full - Current Module"]:
            return self._map_attendance_full(payload, farmer_external_id)
        elif form_name in ["Farmer Registration"]:
            return self._map_farmer_registration(payload, farmer_external_id)
        else:
            raise SkipTransformation(
                f"Unhandled attendance transformation. Form name: '{form_name}'. Skipping payload."
            )

    def _map_attendance_full(self, payload: Dict, farmer_external_id) -> Dict[str, Any]:
        """Map data for Attendance Full - FT"""
        training_session_external_id = payload.get("form", {}).get(
            "training_session", ""
        )
        return {
            "date_attended": payload.get("form", {}).get("date"),
            "status": "Present",
            "submission_id": f"{training_session_external_id}{farmer_external_id}",
        }

    def _map_farmer_registration(
        self, payload: Dict, farmer_external_id
    ) -> Dict[str, Any]:
        """Map data for Farmer Registration"""
        training_session_external_id = payload.get("form", {}).get(
            "training_session", ""
        )
        return {
            "date_attended": payload.get("form", {}).get("registration_date"),
            "status": "Present",
            "submission_id": f"{training_session_external_id}{farmer_external_id}",
        }
