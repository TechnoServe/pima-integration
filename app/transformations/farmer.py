from typing import Dict, Any
from schemas import FarmerCreate
from services import ForeignKeyResolver, SkipTransformation
from models import FarmerGroup, Household
from pydantic import ValidationError
from core import logger


class FarmerTransformer:
    """Transforms CommCare payload to database-ready schema"""

    def __init__(self, resolver: ForeignKeyResolver):
        self.resolver = resolver

    def transform(self, payload: Dict) -> FarmerCreate:
        """Transform CommCare payload to FarmerCreate schema"""

        try:
            # Resolve foreign keys first
            farmer_group_id = self.resolver.resolve_db_id(
                payload.get("form", {}).get("Training_Group_Id"),
                FarmerGroup.commcare_case_id,
                "Farmer Group",
                FarmerGroup
            ).id
            household_id = self.resolver.resolve_db_id(
                payload.get("form", {}).get("Household_Id"),
                Household.tns_id,
                "Household",
                Household,
            ).id

            # Condition for PR Farm Visit Registration
            if (
                payload.get("form", {}).get("survey_type", "") == "Farm Visit Full - PR"
                and payload.get("form", {}).get("new_farmer", "") == "1"
            ):
                farmer_group_id = self.resolver.resolve_db_id(
                    payload.get("form", {})
                    .get("participant_data", {})
                    .get("farmer_registration_details", {})
                    .get("Training_Group_Id", ""),
                    FarmerGroup.commcare_case_id,
                    "Farmer Group",
                    FarmerGroup,
                ).id
                household_id = self.resolver.resolve_db_id(
                    payload.get("form", {})
                    .get("participant_data", {})
                    .get("farmer_registration_details", {})
                    .get("Household_Id", ""),
                    Household.tns_id,
                    "Household",
                    Household,
                ).id

            # Handle different form types and map to appropriate session fields
            session_data = self._map_farmer(payload)

            return FarmerCreate(
                farmer_group_id=farmer_group_id,
                household_id=household_id,
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

    def _map_farmer(self, payload: Dict) -> Dict[str, Any]:
        """Map session data based on form type"""
        survey_type = payload.get("form", {}).get("survey_type", "")
        survey_detail = payload.get("form", {}).get("survey_detail", "")
        pr_registration_fv = (
            survey_type == "Farm Visit Full - PR"
            and payload.get("form", {}).get("new_farmer", "") == "1"
        )
        form_name = payload.get("form", {}).get("@name", "")

        if survey_detail in [
            "New Farmer New Household",
            "New Farmer Existing Household",
        ]:
            return self._map_farmer_registration_new_farmer(payload)
        elif survey_detail in ["Existing Farmer Change in FFG"]:
            return self._map_farmer_registration_change_ffg(payload)
        elif survey_detail in ["Participant Update"]:
            return self._map_farmer_update(payload)
        elif pr_registration_fv:
            return self._map_farmer_registration_pr_fv(payload)
        else:
            raise SkipTransformation(
                f"Unhandled attendance transformation. Form name: '{form_name}'. Skipping payload."
            )

    def _map_farmer_registration_new_farmer(self, payload: Dict) -> Dict[str, Any]:
        """Map data for Farmer - Farmer Registration - NFNH, NFEH"""
        primary_household_member = (
            payload.get("form", {}).get("Primary_Household_Member", "") == "Yes"
        )
        return {
            "tns_id": payload.get("form", {}).get("Farmer_Id"),
            "commcare_case_id": payload.get("form", {})
            .get("subcase_0", {})
            .get("case", {})
            .get("@case_id", ""),
            "first_name": payload.get("form", {}).get("First_Name"),
            "middle_name": payload.get("form", {}).get("Middle_Name", ""),
            "last_name": payload.get("form", {}).get("Last_Name"),
            "other_id": self._get_other_id_number(payload),
            "gender": payload.get("form", {}).get("Gender"),
            "age": int(payload.get("form", {}).get("Age")),
            "phone_number": payload.get("form", {}).get("Phone_Number", ""),
            "is_primary_household_member": primary_household_member,
            "status": "Active",
            "send_to_commcare": False,
            "send_to_commcare_status": "Pending",
        }

    def _map_farmer_registration_change_ffg(self, payload: Dict) -> Dict[str, Any]:
        """Map data for Farmer - Farmer Registration - EFCF"""
        primary_household_member = (
            payload.get("form", {}).get("Primary_Household_Member", "") == "Yes"
        )
        return {
            "tns_id": payload.get("form", {}).get("Farmer_Id"),
            "commcare_case_id": payload.get("form", {})
            .get("existing_farmer_change_in_ffg", {})
            .get("old_farmer_id"),
            "other_id": self._get_other_id_number(payload),
            "is_primary_household_member": primary_household_member,
            "status": "Active",
            "send_to_commcare": False,
            "send_to_commcare_status": "Pending",
        }

    def _map_farmer_update(self, payload: Dict) -> Dict[str, Any]:
        """Map data for Farmer - Edit Farmer Details"""
        primary_household_member = (
            payload.get("form", {}).get("Primary_Household_Member", "") == "Yes"
        )
        return {
            "tns_id": payload.get("form", {}).get("Farmer_Id"), # Not updated
            "commcare_case_id": payload.get("form", {}) # Not updated
            .get("case", {})
            .get("@case_id", ""),
            "first_name": payload.get("form", {}).get("First_Name"), # Not updated
            "middle_name": payload.get("form", {}).get("Middle_Name", ""), # Not updated
            "last_name": payload.get("form", {}).get("Last_Name"), # Not updated
            "other_id": self._get_other_id_number(payload), # Updated
            "gender": payload.get("form", {}).get("Gender"), # Not updated
            "age": int(payload.get("form", {}).get("Age")), # Not updated
            "phone_number": payload.get("form", {}).get("Phone_Number", ""), # Updated
            "is_primary_household_member": primary_household_member, # Not updated
            "status": "Active", # Not updated
            "send_to_commcare": False,
            "send_to_commcare_status": "Pending"
        }

    def _map_farmer_registration_pr_fv(self, payload: Dict) -> Dict[str, Any]:
        """Map data for Farmer - Farmer Registration - PR Farm Visit"""
        payload = payload.get("form", {}).get("participant_data", {}).get("farmer_registration_details", {})
        return {
            "tns_id": payload.get("form", {}).get("Farmer_Id"),
            "commcare_case_id": payload.get("form", {})
            .get("subcase_0", {})
            .get("case", {})
            .get("@case_id", ""),
            "first_name": payload.get("form", {}).get("First_Name"),
            "middle_name": payload.get("form", {}).get("Middle_Name", ""),
            "last_name": payload.get("form", {}).get("Last_Name"),
            "other_id": self._get_other_id_number(payload),
            "gender": payload.get("form", {}).get("Gender"),
            "age": int(payload.get("form", {}).get("Age")),
            "phone_number": payload.get("form", {}).get("Phone_Number", ""),
            "is_primary_household_member": True,
            "status": "Active",
            "send_to_commcare": False,
            "send_to_commcare_status": "Pending",
        }

    def _get_other_id_number(self, payload: Dict) -> str:
        survey_detail = payload.get("form", {}).get("survey_detail", "")
        job_name = payload.get("form", {}).get("@name", "")
        if (
            job_name == "Farmer Registration"
            and survey_detail != "Existing Farmer Change in FFG"
        ) or job_name == "Edit Farmer Details":

            return next(
                (
                    value
                    for value in [
                        payload.get("form", {}).get("National_ID_Number", ""),
                        payload.get("form", {}).get(
                            "Cooperative_Membership_Number", ""
                        ),
                        payload.get("form", {}).get("Grower_Number", ""),
                    ]
                    if value not in ["", None]
                ),
                "",
            )
        else:
            return None
