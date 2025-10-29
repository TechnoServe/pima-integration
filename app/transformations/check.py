"""FIS Coffee Variety JSON Transformer"""

from typing import Dict, Any
from schemas import CheckCreate
from models import FarmVisit, Observation, User, Farmer, TrainingSession
from services import ForeignKeyResolver
from pydantic import ValidationError
from core import logger


class CheckTransformer:
    """Transforms CommCare payload to database-ready schema"""

    def __init__(self, resolver: ForeignKeyResolver):
        self.resolver = resolver

    def transform(
        self, raw_payload: Dict, cleaned_payload: Dict, check_type: str
    ) -> CheckCreate:
        """Transform CommCare payload to CheckCreate schema"""

        try:

            session_data = self._map_check(raw_payload, cleaned_payload, check_type)
            # print(f"Session data: {session_data}")
            if check_type == "Farm Visit":
                farm_visit_id = self.resolver.resolve_db_id(
                    f'FV-{raw_payload.get("id")}',
                    FarmVisit.submission_id,
                    "Farm Visit",
                    FarmVisit,
                ).id

                checker_id = self.resolver.resolve_db_id(
                    raw_payload.get("form", {}).get("trainer"),
                    User.sf_id,
                    "Checker",
                    User,
                ).id

                farmer_id = self.resolver.resolve_db_id(
                    cleaned_payload.get("farmer_id"),
                    Farmer.commcare_case_id,
                    "Farmer",
                    Farmer,
                ).id

                training_session_id = self.resolver.resolve_db_id(
                    raw_payload.get("form", {}).get("training_session"),
                    TrainingSession.commcare_case_id,
                    "Training Session",
                    TrainingSession,
                ).id
                return CheckCreate(
                    farmer_id=farmer_id,
                    farm_visit_id=farm_visit_id,
                    training_session_id=training_session_id,
                    checker_id=checker_id,
                    **session_data,
                )
            elif check_type == "Training Observation":
                observation_id = self.resolver.resolve_db_id(
                    raw_payload.get("id"),
                    Observation.submission_id,
                    "Training Observation",
                    Observation,
                ).id

                checker_id = self.resolver.resolve_db_id(
                    raw_payload.get("form", {}).get("Observer"),
                    User.sf_id,
                    "Checker",
                    User,
                ).id

                farmer_id = self.resolver.resolve_db_id(
                    cleaned_payload.get("participant_id"),
                    Farmer.commcare_case_id,
                    "Farmer",
                    Farmer,
                ).id

                training_session_id = self.resolver.resolve_db_id(
                    raw_payload.get("form", {}).get("selected_session"),
                    TrainingSession.commcare_case_id,
                    "Training Session",
                    TrainingSession,
                ).id
                return CheckCreate(
                    farmer_id=farmer_id,
                    training_session_id=training_session_id,
                    checker_id=checker_id,
                    observation_id=observation_id,
                    **session_data,
                )
            else:
                return CheckCreate(
                    **session_data,
                )
        except ValidationError as e:
            logger.error(
                {"message": "Schema validation failed", "errors": str(e.errors())}
            )
            raise ValueError(f"Schema validation failed: {str(e.errors())}") from e

    def _map_check(
        self, raw_payload: Dict, cleaned_payload: Dict, check_type: str
    ) -> Dict[str, Any]:
        if check_type == "Farm Visit":
            # print("FV Check")
            return self._map_check_fv(raw_payload, cleaned_payload)
        elif check_type == "Training Observation":
            # print("OBS Check")
            return self._map_check_to(raw_payload, cleaned_payload)
        else:
            # print("No Check")
            return {}

    def _map_check_to(self, raw_payload: Dict, cleaned_payload: Dict) -> Dict[str, Any]:
        """Map data for TO Checks"""

        return {
            "submission_id": f'CHK-{raw_payload.get("id")}-{cleaned_payload.get("participant_id", "")}',
            "check_type": "Training Observation",
            "date_completed": raw_payload.get("form", {}).get("Date", ""),
            "attended_last_months_training": {
                "Yes": "Yes",
                "No": "No",
                "No_training_was_offered": "No training was offered",
            }.get(cleaned_payload.get("Attendend_Previous_Training_Module", ""), "N/A"),
        }

    def _map_check_fv(self, raw_payload: Dict, cleaned_payload: Dict) -> Dict[str, Any]:
        """Map data for FV Checks"""

        return {
            "submission_id": f'CHK-{raw_payload.get("id")}-{cleaned_payload.get("farmer_id", "")}',
            "check_type": "Farm Visit",
            "date_completed": raw_payload.get("form", {}).get("date_of_visit", ""),
            "attended_trainings": {"1": "Yes", "0": "No"}.get(
                cleaned_payload.get("attended_training", ""), "N/A"
            ),
            "number_of_trainings_attended": cleaned_payload.get(
                "number_of_trainings", ""
            ),
            "attended_last_months_training": {
                "Yes": "Yes",
                "No": "No",
                "No_training_was_offered": "No training was offered",
            }.get(cleaned_payload.get("Attendend_Previous_Training_Module", ""), "N/A"),
        }
