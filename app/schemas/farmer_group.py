"""Farmer Group Schemas"""

from typing import List, Optional
from pydantic import BaseModel, Field
from uuid import UUID

class FarmerGroupUpdate(BaseModel):
    """Schema for updating farmer group data, mainly for focal and assistant focal farmer assignments"""
    project_id: Optional[UUID] = None
    responsible_staff_id: Optional[UUID] = None
    tns_id: Optional[str] = None
    commcare_case_id: Optional[str] = None
    focal_farmer_id: Optional[UUID] = None
    assistant_focal_farmer_id: Optional[UUID] = None
    ffg_name: Optional[str] = None
    send_to_commcare: Optional[bool] = None
    send_to_commcare_status: Optional[str] = None
    status: Optional[str] = None
    location_id: Optional[UUID] = None
    fv_aa_sampling_round: Optional[int] = None