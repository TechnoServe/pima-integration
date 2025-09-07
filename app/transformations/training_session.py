import datetime
from schemas.training_session import TrainingSessionSchema
from models.training_session import TrainingSession
from core.gps_splitter_util import split_gps

def attendance_light_map(data: dict) -> TrainingSessionSchema:
    
    trainer_sf_id = data.get("form", {}).get("trainer", "")
    date = data.get("form", {}).get("Current_session_participants", {}).get("date", "")
    male_attendees = int(data.get("form", {}).get("Current_session_participants", {}).get("male_attendance", 0))
    female_attendees = int(data.get("form", {}).get("Current_session_participants", {}).get("female_attendance", 0))
    total_attendees = int(data.get("form", {}).get("Current_session_participants", {}).get("total_attendance", 0))
    lat, lon, alt, acc = split_gps(data.get("form", {}).get("gps_coordinates", ""))
    commcare_case_id = data.get("form", {}).get("case", {}).get("@case_id", "")
        
    return TrainingSessionSchema(
        date=datetime.datetime.strptime(date, "%Y-%m-%d") if date else None,
        commcare_case_id=commcare_case_id,
        trainer_sf_id=trainer_sf_id,
        male_attendees=male_attendees,
        female_attendees=female_attendees,
        total_attendees=total_attendees,
        location_gps_latitude=float(lat),
        location_gps_longitude=float(lon),
        location_gps_altitude=float(alt)
    )

def schema_to_model(schema: TrainingSessionSchema) -> TrainingSession:
    return TrainingSession(**schema.model_dump(exclude_unset=True))
