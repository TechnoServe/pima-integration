from typing import Optional
from datetime import date
from decimal import Decimal
from pydantic import BaseModel
from uuid import UUID


class TrainingSessionCreate(BaseModel):
    """Internal schema with resolved IDs for database operations"""

    # Resolved UUIDs (after foreign key resolution)
    trainer_id: UUID  # UUID as string
    module_id: Optional[UUID] = None  # UUID as string
    farmer_group_id: Optional[UUID] = None  # UUID as string

    # Mapped session data
    date_session_1: Optional[date] = None
    date_session_2: Optional[date] = None
    commcare_case_id: str

    male_attendees_session_1: Optional[int] = None
    female_attendees_session_1: Optional[int] = None
    total_attendees_session_1: Optional[int] = None

    male_attendees_session_2: Optional[int] = None
    female_attendees_session_2: Optional[int] = None
    total_attendees_session_2: Optional[int] = None

    male_attendees_agg: Optional[int] = None
    female_attendees_agg: Optional[int] = None
    total_attendees_agg: Optional[int] = None

    location_gps_latitude_session_1: Optional[Decimal] = None
    location_gps_longitude_session_1: Optional[Decimal] = None
    location_gps_altitude_session_1: Optional[Decimal] = None

    location_gps_latitude_session_2: Optional[Decimal] = None
    location_gps_longitude_session_2: Optional[Decimal] = None
    location_gps_altitude_session_2: Optional[Decimal] = None
