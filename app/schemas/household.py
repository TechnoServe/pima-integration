from pydantic import BaseModel
from typing import Optional
import uuid


class HouseholdCreate(BaseModel):
    farmer_group_id: uuid.UUID
    household_name: Optional[str] = None
    household_number: Optional[int] = None
    tns_id: str
    commcare_case_id: Optional[str] = None
    number_of_trees: Optional[int] = 0
    farm_size: Optional[float] = 0.0
    sampled_for_fv_aa: Optional[bool] = False
    farm_size_before: Optional[float] = None
    farm_size_after: Optional[float] = None
    farm_size_since: Optional[float] = None
    status: str
    visited_for_fv_aa: Optional[bool] = False
    fv_aa_sampling_round: Optional[int] = 0

    model_config = {
        "from_attributes": True,
    }
