"""FIS Farm JSON Transformer"""

from datetime import datetime
from typing import Dict, Any
from schemas import FarmCreate
from models import Household, FarmVisit
from services import ForeignKeyResolver
from pydantic import ValidationError
from core import logger


class FarmTransformer:
    """Transforms CommCare payload to database-ready schema"""

    def __init__(self, resolver: ForeignKeyResolver):
        self.resolver = resolver

    def transform(self, raw_payload: Dict, cleaned_payload: Dict) -> FarmCreate:
        """Transform CommCare payload to FarmCreate schema"""

        try:

            session_data = self._map_farm(raw_payload, cleaned_payload)

            # Resolve foreign keys first

            farm_visit_id = self.resolver.resolve_db_id(
                f"FV-{raw_payload.get("id")}",
                FarmVisit.submission_id,
                "Farm Visit",
                FarmVisit,
            ).id
            household_id = None

            # Resolve Household ID using PIMA ID (Could be SF ID or PostgreSQL ID in the future)
            try:
                household_id = self.resolver.resolve_db_id(
                    raw_payload.get("form", {}).get("household_pima_id"),
                    Household.sf_id,
                    "Household",
                    Household,
                ).id
            except ValueError:
                household_id = raw_payload.get("form", {}).get("household_pima_id")

            return FarmCreate(
                farm_visit_id=farm_visit_id,
                household_id=household_id,
                **session_data,
            )
        except ValidationError as e:
            logger.error(
                {"message": "Schema validation failed", "errors": str(e.errors())}
            )
            raise ValueError(f"Schema validation failed: {str(e.errors())}") from e

    def _map_farm(self, raw_payload: Dict, cleaned_payload: Dict) -> Dict[str, Any]:
        """Map data for FIS Farm Data"""

        return {
            "submission_id": f'F-0{cleaned_payload.get("current_index", "")}-{raw_payload.get("form", {}).get("household_pima_id", "")}',
            "farm_name": f"0{cleaned_payload.get("current_index")}",
            "location_gps_latitude": self.parse_gps_coordinates(cleaned_payload).get(
                "latitude"
            ),
            "location_gps_longitude": self.parse_gps_coordinates(cleaned_payload).get(
                "longitude"
            ),
            "location_gps_altitude": self.parse_gps_coordinates(cleaned_payload).get(
                "altitude"
            ),
            "farm_size_coffee_trees": cleaned_payload.get("total_coffee"),
            "farm_size_land_measurements": cleaned_payload.get("farm_size_ha"),
            "main_coffee_field": (
                True
                if cleaned_payload.get("best_practice_plot", None) in ["1", None]
                else False
            ),
            "planting_month_and_year": datetime.strptime(
                cleaned_payload.get("date_planted"), "%Y-%m-%d"
            ).date(),
            "planted_out_of_season": (
                True
                if isinstance(
                    cleaned_payload.get("important_notes_planting_dates", {}), dict
                )
                and cleaned_payload.get("important_notes_planting_dates", {}).get(
                    "planting_period_note_out_of_season", ""
                )
                == "yes"
                else False
            ),
            "tns_id": f'F-0{cleaned_payload.get("current_index", "")}-{raw_payload.get("form", {}).get("household_tns_id", "")}',
            "planted_out_of_season_comments": cleaned_payload.get(
                "important_notes_planting_dates", {}
            ).get("planting_period_comment_out_of_season", "") if isinstance(
                    cleaned_payload.get("important_notes_planting_dates", {}), dict
                ) else None,
            "planted_on_visit_date": (
                True
                if isinstance(
                    cleaned_payload.get("important_notes_planting_dates", {}), dict
                )
                and cleaned_payload.get("important_notes_planting_dates", {}).get(
                    "planting_period_note_same_date_as_visit", ""
                )
                == "yes"
                else False
            ),
        }

    def parse_gps_coordinates(self, payload: Dict) -> Dict[str, Any]:
        """Parse GPS string format: '6.5438677 38.8053416 2255.0 4.5'"""
        gps_coordinates = payload.get("final_gps", "")
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
