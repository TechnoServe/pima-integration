from pydantic import BaseModel
from typing import Optional
from datetime import date
import uuid


class AttendanceCreate(BaseModel):

    farmer_id: uuid.UUID
    training_session_id: uuid.UUID
    date_attended: Optional[date] = None
    status: Optional[str] = None
    submission_id: str
    from_sf: Optional[bool] = False
    sf_id: Optional[str] = None

    model_config = {
        "from_attributes": True,
    }
