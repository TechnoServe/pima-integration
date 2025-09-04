from pydantic import BaseModel, Field
from uuid import UUID
from datetime import date, datetime
from typing import Optional


# ---------- Shared Base ----------
class CheckBase(BaseModel):
    farmer_id: UUID
    submission_id: str
    checker_id: UUID
    observation_id: Optional[UUID] = None
    farm_visit_id: Optional[UUID] = None
    training_session_id: UUID
    check_type: str
    date_completed: date
    attended_trainings: Optional[bool] = None
    number_of_trainings_attended: Optional[int] = None
    attended_last_months_training: Optional[bool] = None
    created_by: UUID
    last_updated_by: UUID
    from_sf: bool = False
    sf_id: Optional[str] = None


# ---------- Create ----------
class CheckCreate(CheckBase):
    """Schema for creating a Check"""
    pass


# ---------- Update ----------
class CheckUpdate(BaseModel):
    """Schema for updating a Check"""
    submission_id: Optional[str] = None
    checker_id: Optional[UUID] = None
    observation_id: Optional[UUID] = None
    farm_visit_id: Optional[UUID] = None
    training_session_id: Optional[UUID] = None
    check_type: Optional[str] = None
    date_completed: Optional[date] = None
    attended_trainings: Optional[bool] = None
    number_of_trainings_attended: Optional[int] = None
    attended_last_months_training: Optional[bool] = None
    last_updated_by: Optional[UUID] = None
    from_sf: Optional[bool] = None
    sf_id: Optional[str] = None


# ---------- Response ----------
class CheckResponse(CheckBase):
    """Schema returned from the API"""
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True  # <-- Pydantic v2 (for ORM mode)
