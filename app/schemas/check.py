from uuid import UUID
from datetime import date
from typing import Optional, Literal
from pydantic import BaseModel


class CheckCreate(BaseModel):
    """Pydantic model for validating the JSON for checks"""

    farmer_id: UUID
    submission_id: str
    checker_id: UUID
    observation_id: Optional[UUID] = None
    farm_visit_id: Optional[UUID] = None
    training_session_id: UUID
    check_type: Literal["Training Observation", "Farm Visit"]
    date_completed: date
    attended_trainings: Optional[bool] = None
    number_of_trainings_attended: Optional[int] = None
    attended_last_months_training: Literal["Yes", "No", "No training was offered"]
