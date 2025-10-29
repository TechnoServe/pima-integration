from pydantic import BaseModel, Field
from typing import Optional, Literal
import uuid


class FarmerCreate(BaseModel):
    household_id: Optional[uuid.UUID] = None
    farmer_group_id: Optional[uuid.UUID] = None
    tns_id: str
    commcare_case_id: str
    first_name: str
    middle_name: Optional[str] = None
    last_name: str
    other_id: Optional[str] = None
    gender: Literal["Male", "Female"]
    age: int = Field(ge=0, le=100)
    phone_number: Optional[str] = None
    is_primary_household_member: bool
    status: Literal["Active", "Inactive"]
    send_to_commcare: bool
    send_to_commcare_status: Literal["Pending", "Processing", "Complete"]
    status_notes: Optional[str] = None
