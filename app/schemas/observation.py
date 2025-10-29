from typing import Optional, Literal
import uuid
from decimal import Decimal
from datetime import date
from pydantic import BaseModel


class ObservationCreate(BaseModel):
    """ Pydantic Schema for validating an Observation JSON from CommCare """
    submission_id: str
    observation_type: Literal["Training", "Demo Plot"]
    observer_id: uuid.UUID
    trainer_id: Optional[uuid.UUID] = None
    farmer_group_id: uuid.UUID
    training_session_id: Optional[uuid.UUID] = None
    observation_date: date
    location_gps_latitude: Decimal
    location_gps_longitude: Decimal
    location_gps_altitude: Decimal
    female_attendees: Optional[int] = None
    male_attendees: Optional[int] = None
    total_attendees: Optional[int] = None
    comments: Optional[str] = None
