from pydantic import BaseModel
from datetime import date
import uuid
from typing import Optional
from decimal import Decimal

class WVSurveyQuestionResponseCreate(BaseModel):
    """ Pydantic Schema for validating a wet mill survey question responses JSON from CommCare """
    survey_response_id: uuid.UUID
    section_name: str
    question_name: str
    field_type: str
    submission_id: str
    value_text: Optional[str]
    value_number: Optional[Decimal]
    value_boolean: Optional[bool]
    value_date: Optional[date]
    value_gps: Optional[str]