from pydantic import BaseModel
from datetime import date
import uuid
from typing import Optional

class WVSurveyResponseCreate(BaseModel):
    """ Pydantic Schema for validating a wet mill survey questions JSON from CommCare """
    form_visit_id: uuid.UUID
    survey_type: str
    completed_date: date
    general_feedback: Optional[str]
    submission_id: str