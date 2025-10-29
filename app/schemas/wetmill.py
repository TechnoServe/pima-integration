from pydantic import BaseModel
from datetime import date
import uuid
from typing import Optional
from decimal import Decimal


class WetmillCreate(BaseModel):
    """Pydantic Schema for validating a wet mill JSON from CommCare"""

    user_id: uuid.UUID
    wet_mill_unique_id: str
    commcare_case_id: str
    name: str
    mill_status: str
    exporting_status: str
    programme: str
    country: str
    manager_name: str
    manager_role: str
    comments: Optional[str]
    wetmill_counter: Optional[Decimal] = None
    ba_signature: str
    manager_signature: str
    tor_page_picture: str
    registration_date: date
    office_entrance_picture: Optional[str]
    office_gps: Optional[object]
