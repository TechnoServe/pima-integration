from pydantic import BaseModel
from datetime import date
import uuid
from typing import Optional
from decimal import Decimal

class WVSurveyQuestionResponseCreate(BaseModel):
    """ Pydantic Schema for validating a wet mill survey question responses JSON from CommCare """
    survey_response_id: uuid.UUID
    section_name: Optional[str]=None
    question_name: str
    field_type: str
    submission_id: str
    value_text: Optional[str]=None
    value_number: Optional[Decimal]=None
    value_boolean: Optional[bool]=None
    value_date: Optional[date]=None
    value_gps: Optional[str]=None