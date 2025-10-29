from typing import Dict, Any
from schemas import HouseholdCreate
from services import ForeignKeyResolver, SkipTransformation
from models import FarmerGroup
from pydantic import ValidationError
from core.logging_util import logger

class HouseholdTransformer:
    """Transforms CommCare payload to database-ready schema"""

    def __init__(self, resolver: ForeignKeyResolver):
        self.resolver = resolver

    def transform(self, payload: Dict) -> HouseholdCreate:
        """Transform CommCare payload to HouseholdCreate schema"""

        try:
            # Resolve foreign keys first
            farmer_group_id = self.resolver.resolve_db_id(
                external_id=payload.get("form", {}).get("Training_Group_Id"),
                id_column=FarmerGroup.commcare_case_id,
                field="Farmer Group",
                model=FarmerGroup,
            ).id

            # Condition for PR Farm Visit Registration
            if (
                payload.get("form", {}).get("survey_type", "") == "Farm Visit Full - PR"
                and payload.get("form", {}).get("new_farmer", "") == "1"
            ):
                farmer_group_id = self.resolver.resolve_db_id(
                    external_id=payload.get("form", {})
                    .get("participant_data", {})
                    .get("farmer_registration_details", {})
                    .get("Training_Group_Id", ""),
                    id_column=FarmerGroup.commcare_case_id,
                    field="Farmer Group",
                    model=FarmerGroup,
                ).id

            # Handle different form types and map to appropriate session fields
            session_data = self._map_household(payload)

            return HouseholdCreate(farmer_group_id=farmer_group_id, **session_data)
        except SkipTransformation as e:
            logger.info(str(e))
            return None
        except ValidationError as e:
            logger.error(
                {"message": "Schema validation failed", "errors": str(e.errors())}
            )
            raise ValueError(f"Schema validation failed: {str(e.errors())}") from e

    def _map_household(self, payload: Dict) -> Dict[str, Any]:
        """Map session data based on form type"""
        survey_type = payload.get("form", {}).get("survey_type", "")
        primary_member = payload.get("form", {}).get("Farmer_Number") == "1"
        survey_detail = payload.get("form", {}).get("survey_detail", "")
        pr_registration_fv = (
            survey_type == "Farm Visit Full - PR"
            and payload.get("form", {}).get("new_farmer", "") == "1"
        )
        form_name = payload.get("form", {}).get("@name", "")

        if (
            survey_detail
            in [
                "New Farmer New Household",
                "New Farmer Existing Household",
                "Existing Farmer Change in FFG",
            ]
            and primary_member
        ):
            return self._map_household_farmer_registration_primary(payload)
        elif (
            survey_detail
            in [
                "New Farmer New Household",
                "New Farmer Existing Household",
                "Existing Farmer Change in FFG",
            ]
            and not primary_member
        ):
            return self._map_household_farmer_registration_secondary(payload)
        elif survey_detail in ["Participant Update"]:
            return self._map_household_farmer_update(payload)
        elif pr_registration_fv:
            return self._map_household_farmer_registration_primary_pr_fv(payload)
        else:
            raise SkipTransformation(
                f"Unhandled attendance transformation. Form name: '{form_name}'. Skipping payload."
            )

    def _map_household_farmer_registration_primary(
        self, payload: Dict
    ) -> Dict[str, Any]:
        """Map data for Household - Farmer Registration and Change in FFG"""
        country = payload.get("form", {}).get("coffee_project_country", "")
        pr = country == "Puerto Rico"
        return {
            "household_name": payload.get("form", {}).get("Household_Number"),
            "household_number": int(payload.get("form", {}).get("Household_Number")),
            "tns_id": payload.get("form", {}).get("Household_Id"),
            "number_of_trees": (
                int(float(self._get_farm_size(payload)))
                if country not in ["Ethiopia"]
                else None
            ),
            "farm_size": (
                float(self._get_farm_size(payload)) if country in ["Ethiopia"] else None
            ),
            "sampled_for_fv_aa": False,
            "farm_size_before": (
                float(
                    payload.get("form", {})
                    .get("participant_data", {})
                    .get("farm_size_3_years_and_older", "")
                )
                if pr
                else None
            ),
            "farm_size_after": (
                float(
                    payload.get("form", {})
                    .get("participant_data", {})
                    .get("farm_size_under_3_years", "")
                )
                if pr
                else None
            ),
            "status": "Active",
            "visited_for_fv_aa": False,
            "fv_aa_sampling_round": 0,
        }

    def _map_household_farmer_registration_secondary(
        self, payload: Dict
    ) -> Dict[str, Any]:
        """Map data for Household - Farmer Registration and Change in FFG"""
        return {
            "household_name": payload.get("form", {}).get("Household_Number"),
            "household_number": int(payload.get("form", {}).get("Household_Number")),
            "tns_id": payload.get("form", {}).get("Household_Id"),
            "status": "Active",
        }

    def _map_household_farmer_registration_primary_pr_fv(
        self, payload: Dict
    ) -> Dict[str, Any]:
        """Map data for Household - Farmer Registration - PR Farm Visit"""
        return {
            "household_name": payload.get("form", {})
            .get("participant_data", {})
            .get("farmer_registration_details", {})
            .get("Household_Number", ""),
            "household_number": int(
                payload.get("form", {})
                .get("participant_data", {})
                .get("farmer_registration_details", {})
                .get("Household_Number", "")
            ),
            "tns_id": payload.get("form", {}).get("Household_Id"),
            "number_of_trees": int(float(self._get_farm_size(payload))),
            "sampled_for_fv_aa": False,
            "farm_size_before": float(
                payload.get("form", {})
                .get("participant_data", {})
                .get("farm_size_3_years_and_older", "")
            ),
            "farm_size_after": float(
                payload.get("form", {})
                .get("participant_data", {})
                .get("farm_size_under_3_years", "")
            ),
            "farm_size_since": 0,
            "status": "Active",
            "visited_for_fv_aa": False,
            "fv_aa_sampling_round": 0,
        }

    def _map_household_farmer_update(self, payload: Dict) -> Dict[str, Any]:
        """Map data for Household - Farmer update"""
        country = payload.get("form", {}).get("coffee_project_country", "")
        return {
            "tns_id": payload.get("form", {}).get("Household_Id"),
            "number_of_trees": (
                int(float(self._get_farm_size(payload)))
                if country not in ["Ethiopia"]
                else None
            ),
            "farm_size": (
                float(self._get_farm_size(payload)) if country in ["Ethiopia"] else None
            ),
            "status": "Active",
        }

    def _get_farm_size(self, payload):
        survey_detail = payload.get("form", {}).get("survey_detail", "")
        job_name = payload.get("form", {}).get("@name", "")
        if (
            job_name == "Farmer Registration"
            and survey_detail != "Existing Farmer Change in FFG"
        ) or job_name in ["Edit Farmer Details", "Field Day Farmer Registration"]:
            return payload.get("form", {}).get("Number_of_Trees") or None
        if (
            payload.get("form", {})
            .get("existing_farmer_change_in_ffg", {})
            .get("former_farmer_primary_secondary_yn")
            == "Yes"
        ):
            return (
                payload.get("form", {})
                .get("existing_farmer_change_in_ffg", {})
                .get("former_farmer_coffeetrees")
                or None
            )
        return None
