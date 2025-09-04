from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime
import uuid

class AttendanceSchema(BaseModel):
    id: Optional[uuid.UUID] = None
    farmer_id: Optional[uuid.UUID] = None
    training_session_id: Optional[uuid.UUID] = None
    date_attended: Optional[date] = None
    status: Optional[bool] = None
    submission_id: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    created_by: Optional[uuid.UUID] = None
    last_updated_by: Optional[uuid.UUID] = None
    from_sf: Optional[bool] = False
    sf_id: Optional[str] = None

    model_config = {
        "from_attributes": True,
    }