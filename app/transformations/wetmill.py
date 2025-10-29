from core import (
    logger,
    map_status, map_mill_status, map_manager_role, EXPORTING_STATUS_MAP, MANAGER_ROLE_MAP, WET_MILL_STATUS_MAP, VERTICAL_INTEGRATION_MAP
)
from schemas import WetmillCreate
from models import ProjectStaffRole
from services import ForeignKeyResolver
from pydantic import ValidationError
from geoalchemy2.shape import from_shape
from shapely.geometry import Point


class WetmillTransformer:
    def __init__(self, resolver: ForeignKeyResolver):
        self.resolver = resolver

    def transform(self, payload: dict) -> WetmillCreate:
        """Transform CommCare payload to WetmillCreate schema"""
        form = payload.get("form", {})
        case = form.get("case", {})
        case_id = case.get("@case_id")

        try:
            # Lookup/create Wetmill
            user_id = self.resolver.resolve_db_id(
                case_id,
                ProjectStaffRole.commcare_case_id,
                "Project Role",
                ProjectStaffRole,
            ).staff_id

            session_data = self._map_wetmill_data(payload=payload)

            return WetmillCreate(
                user_id=user_id, **session_data
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

    def _map_wetmill_data(self, payload: dict) -> dict:
        form = payload["form"]
        wetmill_details = form.get("wet_mill_details", {})

        location = wetmill_details.get("office_gps", None)
        point = self._extract_location_string(location)

        exporting_status = map_status(
            wetmill_details.get("exporting_status", "N/A"), EXPORTING_STATUS_MAP
        )
        
        vertical_integration = map_status(
            wetmill_details.get("vertical_integration", "N/A"), VERTICAL_INTEGRATION_MAP
        )
        
        wet_mill_status = map_mill_status(
            wetmill_details.get("mill_status"), 
            WET_MILL_STATUS_MAP,
            form.get("survey_type", ""),
        )
        manager_role = map_manager_role(
            wetmill_details.get("manager_role"),
            MANAGER_ROLE_MAP,
            wetmill_details.get("manager_role_other"),
            form.get("survey_type")
        )
        
        wet_mill_unique_id = form.get("wetmill_tns_id")
        if not wet_mill_unique_id:
            raise ValueError("Missing wetmill_tns_id")
        
        commcare_case_id = form.get("subcase_0", {}).get("case", {}).get("@case_id")
        entrance_picture = wetmill_details.get("office_entrance_picture")
        tor_picture = wetmill_details.get("tor_page_picture")
        ba_signature = wetmill_details.get("ba_signature")
        manager_signature = wetmill_details.get("manager_signature")
        
        return {
            "wet_mill_unique_id": wet_mill_unique_id,
            "commcare_case_id": commcare_case_id,
            "name": wetmill_details.get("mill_registered_name"),
            "mill_status": wet_mill_status,
            "exporting_status": exporting_status,
            "manager_name": wetmill_details.get("manager_name"),
            "comments": wetmill_details.get("comments"),
            "ba_signature": payload.get("attachments", {}).get(ba_signature, {}).get("url", "") if ba_signature else None,
            "manager_signature": payload.get("attachments", {}).get(manager_signature, {}).get("url", "") if manager_signature else None,
            "tor_page_picture": payload.get("attachments", {}).get(tor_picture, {}).get("url", "") if tor_picture else None,
            "manager_role": manager_role,
            "programme": form.get("programme"),
            "country": form.get("country"),
            "registration_date": form.get("registration_date"),
            "office_entrance_picture": payload.get("attachments", {}).get(entrance_picture, {}).get("url", "") if entrance_picture else None,
            "office_gps": from_shape(point, srid=4326) if point else None,
            "vertical_integration": vertical_integration
    }

    def _extract_location_string(self, location_string):
        """
        Parse a GPS string "lat lon ..." into a Shapely Point (lon, lat).
        """
        try:
            lat, lon, *_ = map(float, location_string.split())
            return Point(lon, lat)
        except Exception as e:
            return None
