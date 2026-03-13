"""Farmer Group Transformations"""

from models import Farmer, FarmerGroup
from schemas import FarmerGroupUpdate
from pydantic import ValidationError
from services import ForeignKeyResolver
from core import logger

class FarmerGroupTransformer:
    """Transforms CommCare payload to database-ready schema"""
    def __init__(self, resolver: ForeignKeyResolver):
            self.resolver = resolver
    
    def transform(self, payload: dict) -> FarmerGroupUpdate:
        """Transform CommCare payload to FarmerGroupUpdate schema"""
        try:
            
            data = self._map_form_type(payload)
            results = {
                "commcare_case_id": data.get("commcare_case_id"),
            }
            
            focal_farmer_id = self.resolver.resolve_db_id(
                data.get("focal_farmer_case_id"),
                Farmer.commcare_case_id,
                "Focal Farmer",
                Farmer,
            ).id if data.get("focal_farmer_case_id") else None
            
            assistant_focal_farmer_id = self.resolver.resolve_db_id(
                data.get("assistant_focal_farmer_case_id"),
                Farmer.commcare_case_id,
                "Assistant Focal Farmer",
                Farmer,
            ).id if data.get("assistant_focal_farmer_case_id") else None
            
            if focal_farmer_id:
                results["focal_farmer_id"] = focal_farmer_id
            if assistant_focal_farmer_id:
                results["assistant_focal_farmer_id"] = assistant_focal_farmer_id
        
            return FarmerGroupUpdate(**results)
        except ValidationError as e:
            logger.error(f"Validation error while transforming farmer group data: {e}")
            raise
    def _map_form_type(self, payload: dict) -> dict:
        form_type = payload.get("form", {}).get("survey_type", "")
        if form_type == "Attendance Full":
            return {
                "focal_farmer_case_id": payload.get("form", {}).get("updated_focal_farmer_case_id"),
                "assistant_focal_farmer_case_id": payload.get("form", {}).get("updated_assistant_focal_farmer_case_id"),
                "commcare_case_id": payload.get("form", {}).get("ffg_case_id")
            }
        elif form_type == "Participant":
            new_farmer_yn = payload.get("form", {}).get("create_case", "") == "Yes"
            farmer_commcare_case_id = payload.get("form", {}).get("subcase_0", {}).get("case", {}).get("@case_id", "") if new_farmer_yn else payload.get("form", {}).get("existing_farmer_change_in_ffg", {}).get("old_farmer_id")
            is_focal_farmer = payload.get("form", {}).get("Farmer_Role", "") == "Focal Farmer"
            is_assistant_focal_farmer = payload.get("form", {}).get("Farmer_Role", "") == "Assistant Focal Farmer"
            return {
                "focal_farmer_case_id": farmer_commcare_case_id if is_focal_farmer else None,
                "assistant_focal_farmer_case_id": farmer_commcare_case_id if is_assistant_focal_farmer else None,
                "commcare_case_id": payload.get("form", {}).get("case", {}).get("@case_id", "")
            }
