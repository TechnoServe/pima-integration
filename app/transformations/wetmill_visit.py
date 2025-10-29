from core import (
    SessionLocal,
    logger,
)
from schemas import WetmillVisitCreate
from models import Wetmill
from services import ForeignKeyResolver
import datetime
from pydantic import ValidationError
from geoalchemy2.shape import from_shape
from shapely.geometry import Point


class WetmillVisitTransformer:
    def __init__(self, db=SessionLocal):
        self.resolver = ForeignKeyResolver(db)

    def transform(self, payload: dict) -> WetmillVisitCreate:
        """Transform CommCare payload to TrainingSessionCreate schema"""
        form = payload.get("form", {})
        case = form.get("case", {})
        case_id = case.get("@case_id")

        try:
            # Lookup/create Wetmill
            wetmill = self.resolver.resolve_db_id(
                case_id,
                Wetmill.commcare_case_id,
                "Wetmill",
                Wetmill,
            )

            session_data = self._map_wetmill_visit_data(payload=payload)

            return WetmillVisitCreate(
                wetmill_id=wetmill.id, user_id=wetmill.user_id, **session_data
            )

        except ValidationError as e:
            logger.error(
                {"message": "Schema validation failed", "errors": str(e.errors())}
            )
            raise ValueError(f"Schema validation failed: {str(e.errors())}") from e
        except Exception as e:
            logger.error(
                {"message": "Unhandled transformation error", "errors": str(e)}
            )
            raise

    def _map_wetmill_visit_data(self, payload: dict) -> dict:
        form = payload.get("form", {})
        visit_date_str = form.get("date")
        visit_date = (
            datetime.datetime.strptime(visit_date_str, "%Y-%m-%d")
            if visit_date_str
            else None
        )
        form_name = form.get("survey_type")
        form_id = payload.get("id")
        loc_str = form.get("introduction", {}).get("gps", "")
        point = self.extract_location_string(loc_str)
        entrance_photograph = (
            payload.get("attachments", {})
            .get(
                payload.get("form", {})
                .get("introduction", {})
                .get("wetmill_entrance_photograph")
            )
            .get("url", "")
        )
        return {
            "submission_id": f"WV-{form_id}",
            "form_name": form_name,
            "visit_date": visit_date,
            "entrance_photograph": entrance_photograph,
            "geo_location": from_shape(point, srid=4326) if point else None,
        }

    def extract_location_string(self, location_string):
        """
        Parse a GPS string "lat lon ..." into a Shapely Point (lon, lat).
        """
        try:
            lat, lon, *_ = map(float, location_string.split())
            return Point(lon, lat)
        except Exception as e:
            return None
