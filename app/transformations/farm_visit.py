"""Farm Visit JSON Transformer"""

from typing import Dict, Any
from schemas import FarmVisitCreate
from models import Household, Farmer, TrainingSession, User
from services import ForeignKeyResolver
from pydantic import ValidationError
from core import logger


class FarmVisitTransformer:
    """Transforms CommCare payload to database-ready schema"""

    def __init__(self, resolver: ForeignKeyResolver):
        self.resolver = resolver

    def transform(self, payload: Dict) -> FarmVisitCreate:
        """Transform CommCare payload to FarmVisitCreate schema"""

        try:

            session_data = self._map_farm_visit_full(payload)
            survey_detail = payload.get("form", {}).get("@name")
            new_farmer = payload.get("form", {}).get("new_farmer", "") == "1"

            # Resolve foreign keys first
            visiting_staff_id = self.resolver.resolve_db_id(
                payload.get("form", {}).get("trainer"),
                User.sf_id,
                "Visiting Staff",
                User,
            ).id
            # Condition for PR Farm Visit Registration
            if survey_detail == "Farm Visit Full" and new_farmer:
                visited_household_id = self.resolver.resolve_db_id(
                    payload.get("form", {})
                    .get("participant_data", {})
                    .get("farmer_registration_details", {})
                    .get("Household_Id"),
                    Household.tns_id,
                    "Household",
                    Household,
                ).id
                visited_primary_farmer_id = self.resolver.resolve_db_id(
                    payload.get("form", {})
                    .get("subcase_0", {})
                    .get("case", {})
                    .get("@case_id", ""),
                    Farmer.commcare_case_id,
                    "Primary Farmer",
                    Farmer,
                ).id

                return FarmVisitCreate(
                    visited_primary_farmer_id=visited_primary_farmer_id,
                    visited_household_id=visited_household_id,
                    visiting_staff_id=visiting_staff_id,
                    **session_data,
                )
            if survey_detail == "Farm Visit Full" and not new_farmer:

                visited_primary_farmer_id = self.resolver.resolve_db_id(
                    payload.get("form", {}).get("farm_being_visted", ""),
                    Farmer.commcare_case_id,
                    "Primary Farmer",
                    Farmer,
                ).id
                visited_household_id = self.resolver.resolve_db_id(
                    payload.get("form", {}).get("farm_being_visted", ""),
                    Farmer.commcare_case_id,
                    "Primary Farmer",
                    Farmer,
                ).household_id
                secondary_farmer = payload.get("form", {}).get("secondary_farmer")

                training_session_id = self.resolver.resolve_db_id(
                    payload.get("form", {}).get("training_session"),
                    TrainingSession.commcare_case_id,
                    "Training Session",
                    TrainingSession,
                ).id

                if secondary_farmer:
                    visited_secondary_farmer_id = self.resolver.resolve_db_id(
                        secondary_farmer,
                        Farmer.commcare_case_id,
                        "Secondary Farmer",
                        Farmer,
                    ).id

                    return FarmVisitCreate(
                        visited_household_id=visited_household_id,
                        visited_primary_farmer_id=visited_primary_farmer_id,
                        visited_secondary_farmer_id=visited_secondary_farmer_id,
                        training_session_id=training_session_id,
                        visiting_staff_id=visiting_staff_id,
                        **session_data,
                    )
                else:
                    return FarmVisitCreate(
                        visited_household_id=visited_household_id,
                        visited_primary_farmer_id=visited_primary_farmer_id,
                        training_session_id=training_session_id,
                        visiting_staff_id=visiting_staff_id,
                        **session_data,
                    )

            if survey_detail == "Farm Visit - AA":

                farmers_present = payload.get("form", {}).get("farm_being_visted", "")
                farmers_list = farmers_present.split(" ") if farmers_present else []
                primary_farmer = farmers_list[0] if len(farmers_list) > 0 else ""
                secondary_farmer = farmers_list[1] if len(farmers_list) > 1 else ""

                visited_primary_farmer_id = self.resolver.resolve_db_id(
                    primary_farmer,
                    Farmer.commcare_case_id,
                    "Primary Farmer",
                    Farmer,
                ).id
                visited_household_id = self.resolver.resolve_db_id(
                    primary_farmer,
                    Farmer.commcare_case_id,
                    "Primary Farmer",
                    Farmer,
                ).household_id

                training_session_id = self.resolver.resolve_db_id(
                    payload.get("form", {}).get("training_session"),
                    TrainingSession.commcare_case_id,
                    "Training Session",
                    TrainingSession,
                ).id

                if secondary_farmer:
                    visited_secondary_farmer_id = self.resolver.resolve_db_id(
                        secondary_farmer,
                        Farmer.commcare_case_id,
                        "Secondary Farmer",
                        Farmer,
                    ).id

                    return FarmVisitCreate(
                        visited_household_id=visited_household_id,
                        visited_primary_farmer_id=visited_primary_farmer_id,
                        visited_secondary_farmer_id=visited_secondary_farmer_id,
                        training_session_id=training_session_id,
                        visiting_staff_id=visiting_staff_id,
                        **session_data,
                    )
                else:
                    return FarmVisitCreate(
                        visited_household_id=visited_household_id,
                        visited_primary_farmer_id=visited_primary_farmer_id,
                        training_session_id=training_session_id,
                        visiting_staff_id=visiting_staff_id,
                        **session_data,
                    )
            else:
                return FarmVisitCreate(
                    **session_data,
                )
        except ValidationError as e:
            logger.error(
                {"message": "Schema validation failed", "errors": str(e.errors())}
            )
            raise ValueError(f"Schema validation failed: {str(e.errors())}") from e

    def _map_farm_visit_full(self, payload: Dict) -> Dict[str, Any]:
        """Map data for Farm Visit Full for FT submissions"""

        return {
            "submission_id": f"FV-{payload.get("id")}",
            "date_visited": payload.get("form", {}).get("date_of_visit", ""),
            "farm_visit_type": payload.get("form", {}).get("survey_type", ""),
            "visit_comments": payload.get("form", {}).get("farm_visit_comments", ""),
            "latest_visit": True,
            "location_gps_latitude": self.parse_gps_coordinates(payload).get(
                "latitude"
            ),
            "location_gps_longitude": self.parse_gps_coordinates(payload).get(
                "longitude"
            ),
            "location_gps_altitude": self.parse_gps_coordinates(payload).get(
                "altitude"
            ),
        }

    def parse_gps_coordinates(self, payload: Dict) -> Dict[str, Any]:
        """Parse GPS string format: '6.5438677 38.8053416 2255.0 4.5'"""
        gps_coordinates = (
            payload.get("form", {})
            .get("best_practice_questions", {})
            .get("gps_coordinates")
            if payload.get("form", {}).get("survey_type", "") == "Farm Visit Full - ET"
            else payload.get("form", {}).get("gps_coordinates")
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
