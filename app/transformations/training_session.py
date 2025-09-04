import datetime
from schemas.training_session import TrainingSessionSchema
from models.training_session import TrainingSession
from app.core.gps_splitter_util import split_gps

def attendance_light_ft_map(data: dict) -> TrainingSessionSchema:
    
    date = data.get("form", {}).get("Current_session_participants", {}).get("date", "")
    male_attendees = int(data.get("form", {}).get("Current_session_participants", {}).get("male_attendance", 0))
    female_attendees = int(data.get("form", {}).get("Current_session_participants", {}).get("female_attendance", 0))
    total_attendees = int(data.get("form", {}).get("Current_session_participants", {}).get("total_attendance", 0))
    lat, lon, alt, acc = split_gps(data.get("form", {}).get("gps_coordinates", ""))
    commcare_case_id = data.get("form", {}).get("case", {}).get("@case_id", "")
    return TrainingSessionSchema(
        commcare_case_id=commcare_case_id,
        trainer_id=None,  # Placeholder, to be resolved later
        date_session_1=datetime.datetime.strptime(date, "%Y-%m-%d") if date else None,
        male_attendees_session_1=male_attendees,
        female_attendees_session_1=female_attendees,
        total_attendees_session_1=total_attendees,
        location_gps_latitude_session_1=float(lat),
        location_gps_longitude_session_1=float(lon),
        location_gps_altitude_session_1=float(alt),
        send_to_commcare=False,
        created_at=None,  # Placeholder, to be set later
        updated_at=None,  # Placeholder, to be set later
        created_by=None,  # Placeholder, to be set later
        last_updated_by=None  # Placeholder, to be set later
    )

def attendance_light_aa_map(data: dict) -> TrainingSessionSchema:
    date = data.get("form", {}).get("Current_session_participants", {}).get("date", "")
    male_attendees = int(data.get("form", {}).get("Current_session_participants", {}).get("male_attendance", 0))
    female_attendees = int(data.get("form", {}).get("Current_session_participants", {}).get("female_attendance", 0))
    total_attendees = int(data.get("form", {}).get("Current_session_participants", {}).get("total_attendance", 0))
    lat, lon, alt, acc = split_gps(data.get("form", {}).get("gps_coordinates", ""))
    
    return TrainingSessionSchema(
        trainer_id=None,  # Placeholder, to be resolved later
        date_session_2=datetime.datetime.strptime(date, "%Y-%m-%d") if date else None,
        male_attendees_session_2=male_attendees,
        female_attendees_session_2=female_attendees,
        total_attendees_session_2=total_attendees,
        location_gps_latitude_session_2=lat,
        location_gps_longitude_session_2=lon,
        location_gps_altitude_session_2=alt,
        send_to_commcare=False,
        created_at=None,  # Placeholder, to be set later
        updated_at=None,  # Placeholder, to be set later
        created_by=None,  # Placeholder, to be set later
        last_updated_by=None  # Placeholder, to be set later
    )
def schema_to_model(schema: TrainingSessionSchema) -> TrainingSession:
    return TrainingSession(**schema.model_dump(exclude_unset=True))
