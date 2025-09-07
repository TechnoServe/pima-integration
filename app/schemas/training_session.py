from pydantic import BaseModel
from datetime import date

class TrainingSessionSchema(BaseModel):
    date: date
    commcare_case_id: str
    trainer_sf_id: str
    male_attendees: int
    female_attendees: int
    total_attendees: int
    location_gps_latitude: float
    location_gps_longitude: float
    location_gps_altitude: float

    model_config = {
        "from_attributes": True,
    }
    
