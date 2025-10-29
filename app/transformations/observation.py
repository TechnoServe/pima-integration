from typing import Dict, Any
from schemas import ObservationCreate
from services import ForeignKeyResolver
from models import User, FarmerGroup, TrainingSession
from core import logger
from pydantic import ValidationError


class ObservationTransformer:
    """Transforms CommCare payload to database-ready schema"""

    def __init__(self, resolver: ForeignKeyResolver):
        self.resolver = resolver

    def transform(self, payload: Dict) -> ObservationCreate:
        """Transform CommCare payload to ObservationCreate schema"""
        try:
            session_data = self._map_observation_data(payload)

            if (
                payload.get("form", {}).get("survey_type", "")
                == "Training Observation - Agronomy"
            ):

                trainer_id = self.resolver.resolve_db_id(
                    payload.get("form", {}).get("trainer_salesforce_id"),
                    id_column=User.sf_id,
                    field="Trainer",
                    model=User,
                ).id
                observer_id = self.resolver.resolve_db_id(
                    external_id=payload.get("form", {}).get("Observer", ""),
                    id_column=User.sf_id,
                    field="Observer",
                    model=User,
                ).id
                farmer_group_id = self.resolver.resolve_db_id(
                    payload.get("form", {}).get(
                        "Which_Group_Is_Farmer_Trainer_Teaching", ""
                    ),
                    id_column=FarmerGroup.commcare_case_id,
                    field="Training Group",
                    model=FarmerGroup,
                ).id
                training_session_id = self.resolver.resolve_db_id(
                    external_id=payload.get("form", {}).get("selected_session", ""),
                    id_column=TrainingSession.commcare_case_id,
                    field="Training Session",
                    model=TrainingSession,
                ).id
                return ObservationCreate(
                    observer_id=observer_id,
                    farmer_group_id=farmer_group_id,
                    training_session_id=training_session_id,
                    trainer_id=trainer_id,
                    **session_data,
                )
            if (
                payload.get("form", {}).get("survey_type", "")
                == "Demo Plot Observation"
            ):
                observer_id = self.resolver.resolve_db_id(
                    payload.get("form", {}).get("observer", ""),
                    id_column=User.sf_id,
                    field="Observer",
                    model=User,
                ).id
                farmer_group_id = self.resolver.resolve_db_id(
                    external_id=payload.get("form", {}).get("training_group", ""),
                    id_column=FarmerGroup.commcare_case_id,
                    field="Training Group",
                    model=FarmerGroup,
                ).id
                return ObservationCreate(
                    observer_id=observer_id,
                    farmer_group_id=farmer_group_id,
                    **session_data,
                ).id

            # return ObservationCreate(**session_data)

        except ValidationError as e:
            logger.error(
                {"message": "Schema validation failed", "errors": str(e.errors())}
            )
            raise ValueError(f"Schema validation failed: {str(e.errors())}") from e

    def _map_observation_data(self, payload: Dict) -> Dict[str, Any]:
        """Map session data based on form type"""
        survey_type = payload.get("form", {}).get("survey_type", "")

        if survey_type == "Training Observation - Agronomy":
            return self._map_training_observation(payload)
        if survey_type == "Demo Plot Observation":
            return self._map_demoplot_observation(payload)
        return {}

    def _map_training_observation(self, payload: Dict) -> Dict[str, Any]:
        """Map data for Training Observation Form"""
        return {
            "submission_id": payload.get("id"),
            "observation_type": "Training",
            "observation_date": payload.get("form", {}).get("Date", ""),
            "location_gps_latitude": self.parse_gps_coordinates(payload).get(
                "latitude"
            ),
            "location_gps_longitude": self.parse_gps_coordinates(payload).get(
                "longitude"
            ),
            "location_gps_altitude": self.parse_gps_coordinates(payload).get(
                "altitude"
            ),
            "female_attendees": int(
                float(
                    payload.get("form", {})
                    .get("Current_session_participants", {})
                    .get("Female_Participants_In_Attendance", "")
                )
            ),
            "male_attendees": int(
                float(
                    payload.get("form", {})
                    .get("Current_session_participants", {})
                    .get("Male_Participants_In_Attendance", "")
                )
            ),
            "total_attendees": int(
                float(
                    payload.get("form", {})
                    .get("Current_session_participants", {})
                    .get("Total_Participants_In_Attendance", "")
                )
            ),
            "comments": f"Did Well: '{payload.get("form", {}).get("case", {}).get("update", {}).get("Did_Well", "")}'; To Improve: '{payload.get("form", {}).get("case", {}).get("update", {}).get("To_Improve", "")}'",
        }

    def _map_demoplot_observation(self, payload: Dict) -> Dict[str, Any]:
        """Map data for Demo Plot Observation Form"""
        return {
            "submission_id": payload.get("id"),
            "observation_type": "Demo Plot",
            "observation_date": payload.get("form", {}).get("date", ""),
            "location_gps_latitude": self.parse_gps_coordinates(payload).get(
                "latitude"
            ),
            "location_gps_longitude": self.parse_gps_coordinates(payload).get(
                "longitude"
            ),
            "location_gps_altitude": self.parse_gps_coordinates(payload).get(
                "altitude"
            ),
            "comments": payload.get("form", {}).get("visit_comments", ""),
        }

    def parse_gps_coordinates(self, payload: Dict) -> Dict[str, Any]:
        """Parse GPS string format: '6.5438677 38.8053416 2255.0 4.5'"""
        gps_coordinates = payload.get("form", {}).get("meta", {}).get(
            "location", {}
        ).get("#text") or payload.get("form", {}).get("gps_information", {}).get(
            "gps_location"
        )
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
