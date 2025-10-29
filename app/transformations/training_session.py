from typing import Dict, Any
from schemas import TrainingSessionCreate
from services import ForeignKeyResolver
from models import User
from core.logging_util import logger
from pydantic import ValidationError


class TrainingSessionTransformer:
    """Transforms CommCare payload to database-ready schema"""

    def __init__(self, resolver: ForeignKeyResolver):
        self.resolver = resolver

    def transform(self, payload: Dict) -> TrainingSessionCreate:
        """Transform CommCare payload to TrainingSessionCreate schema"""
        try:
            trainer_id = self.resolver.resolve_db_id(
                external_id=payload.get("form", {}).get("trainer"),
                id_column=User.sf_id,
                field="Trainer",
                model=User,
            ).id

            session_data = self._map_session_data(payload)

            return TrainingSessionCreate(trainer_id=trainer_id, **session_data)

        except ValidationError as e:
            logger.error(
                {"message": "Schema validation failed", "errors": str(e.errors())}
            )
            raise ValueError(f"Schema validation failed: {str(e.errors())}") from e

    def _map_session_data(self, payload: Dict) -> Dict[str, Any]:
        """Map session data based on form type"""
        form_name = payload.get("form", {}).get("@name", "")
        survey_type = payload.get("form", {}).get("survey_type", "")
        survey_detail = payload.get("form", {}).get("survey_detail", "")
        session = payload.get("form", {}).get("session", "")

        if (
            form_name == "Attendance Light - Current Module"
            or (form_name == "Followup" and survey_type == "Attendance Light")
        ) and session in ["first_session", None, ""]:
            return self._map_ft_light_session(payload)
        elif (
            form_name == "Attendance Light - Current Module"
            or (form_name == "Followup" and survey_type == "Attendance Light")
        ) and session == "second_session":
            return self._map_aa_light_session(payload)
        elif form_name == "Attendance Full - Current Module":
            return self._map_ft_full_session(payload)
        elif survey_detail in [
            "New Farmer New Household",
            "New Farmer Existing Household",
            "Existing Farmer Change in FFG",
        ]:
            return self._map_farmer_registration(payload)
        else:
            # Default mapping
            return self._map_default_session(payload)

    def _map_ft_light_session(self, payload: Dict) -> Dict[str, Any]:
        """Map data for Attendance Light - FT (session 1 fields)"""
        return {
            "commcare_case_id": payload.get("form", {}).get(
                "selected_training_module", ""
            ),
            "date_session_1": payload.get("form", {})
            .get("Current_session_participants", {})
            .get("date", ""),
            "male_attendees_session_1": payload.get("form", {})
            .get("Current_session_participants", {})
            .get("male_attendance", ""),
            "female_attendees_session_1": payload.get("form", {})
            .get("Current_session_participants", {})
            .get("female_attendance", ""),
            "total_attendees_session_1": payload.get("form", {})
            .get("Current_session_participants", {})
            .get("total_attendance", ""),
            "location_gps_latitude_session_1": self.parse_gps_coordinates(payload).get(
                "latitude"
            ),
            "location_gps_longitude_session_1": self.parse_gps_coordinates(payload).get(
                "longitude"
            ),
            "location_gps_altitude_session_1": self.parse_gps_coordinates(payload).get(
                "altitude"
            ),
        }

    def _map_aa_light_session(self, payload: Dict) -> Dict[str, Any]:
        """Map data for Attendance Light - AA (session 2 fields)"""
        return {
            "commcare_case_id": payload.get("form", {}).get(
                "selected_training_module", ""
            ),
            "date_session_2": payload.get("form", {})
            .get("Current_session_participants", {})
            .get("date", ""),
            "male_attendees_session_2": payload.get("form", {})
            .get("Current_session_participants", {})
            .get("male_attendance", ""),
            "female_attendees_session_2": payload.get("form", {})
            .get("Current_session_participants", {})
            .get("female_attendance", ""),
            "total_attendees_session_2": payload.get("form", {})
            .get("Current_session_participants", {})
            .get("total_attendance", ""),
            "location_gps_latitude_session_2": self.parse_gps_coordinates(payload).get(
                "latitude"
            ),
            "location_gps_longitude_session_2": self.parse_gps_coordinates(payload).get(
                "longitude"
            ),
            "location_gps_altitude_session_2": self.parse_gps_coordinates(payload).get(
                "altitude"
            ),
        }

    def _map_ft_full_session(self, payload: Dict) -> Dict[str, Any]:
        """Map data for Attendance Full - FT (session 1 fields)"""
        return {
            "commcare_case_id": payload.get("form", {}).get("training_session", ""),
            "date_session_1": payload.get("form", {}).get("date"),
            "location_gps_latitude_session_1": self.parse_gps_coordinates(payload).get(
                "latitude"
            ),
            "location_gps_longitude_session_1": self.parse_gps_coordinates(payload).get(
                "longitude"
            ),
            "location_gps_altitude_session_1": self.parse_gps_coordinates(payload).get(
                "altitude"
            ),
        }

    def _map_farmer_registration(self, payload: Dict) -> Dict[str, Any]:
        """Map data for Attendance Full - FT (session 1 fields)"""
        return {
            "commcare_case_id": payload.get("form", {}).get(
                "selected_training_module", ""
            ),
            "date_session_1": payload.get("form", {}).get("date"),
        }

    def _map_default_session(self, payload: Dict) -> Dict[str, Any]:
        """Default mapping when form type is unknown"""
        return {
            "date_session_1": payload.session_date_1,
            "date_session_2": payload.session_date_2,
            "male_attendees_session_1": payload.male_attendees,
            "female_attendees_session_1": payload.female_attendees,
            "total_attendees_session_1": payload.total_attendees,
        }

    def parse_gps_coordinates(self, payload: Dict) -> Dict[str, Any]:
        """Parse GPS string format: '6.5438677 38.8053416 2255.0 4.5'"""
        gps_coordinates = payload.get("form", {}).get("gps_coordinates")
        if not gps_coordinates:
            return {"latitude": None, "longitude": None, "altitude": None}

        try:
            parts = gps_coordinates.strip().split()
            return {
                "latitude": float(str(parts[0])) if len(parts) > 0 else None,
                "longitude": float(str(parts[1])) if len(parts) > 1 else None,
                "altitude": float(str(parts[2])) if len(parts) > 2 else None,
            }
        except (ValueError, IndexError):
            return {"latitude": None, "longitude": None, "altitude": None}
