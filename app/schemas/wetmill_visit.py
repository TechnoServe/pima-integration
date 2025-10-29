from pydantic import BaseModel
from datetime import date
import uuid

class WetmillVisitCreate(BaseModel):
    """ Pydantic Schema for validating a wet mill visit JSON from CommCare """
    wetmill_id: uuid.UUID
    user_id: uuid.UUID
    form_name: str
    visit_date: date
    entrance_photograph: str
    geo_location: object
    submission_id: str