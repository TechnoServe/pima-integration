from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime
import uuid

class TrainingSessionSchema(BaseModel):
    id: Optional[uuid.UUID] = None
    trainer_id: Optional[uuid.UUID]
    module_id: Optional[uuid.UUID] = None
    farmer_group_id: Optional[uuid.UUID] = None

    date_session_1: Optional[date] = None
    date_session_2: Optional[date] = None
    commcare_case_id: Optional[str]
    
    male_attendees_session_1: Optional[int] = 0
    female_attendees_session_1: Optional[int] = 0
    total_attendees_session_1: Optional[int] = 0
    
    male_attendees_session_2: Optional[int] = 0
    female_attendees_session_2: Optional[int] = 0
    total_attendees_session_2: Optional[int] = 0

    male_attendees_agg: Optional[int] = 0
    female_attendees_agg: Optional[int] = 0
    total_attendees_agg: Optional[int] = 0

    location_gps_latitude_session_1: Optional[float] = None
    location_gps_longitude_session_1: Optional[float] = None
    location_gps_altitude_session_1: Optional[float] = None
    
    location_gps_latitude_session_2: Optional[float] = None
    location_gps_longitude_session_2: Optional[float] = None
    location_gps_altitude_session_2: Optional[float] = None

    send_to_commcare: Optional[bool] = False
    send_to_commcare_status: Optional[str] = None

    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    created_by: Optional[uuid.UUID]
    last_updated_by: Optional[uuid.UUID]

    model_config = {
        "from_attributes": True,
    }
