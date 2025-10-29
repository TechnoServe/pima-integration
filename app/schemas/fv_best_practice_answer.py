from typing import Optional
from decimal import Decimal
from uuid import UUID
from pydantic import BaseModel


class FVBestPracticeAnswerCreate(BaseModel):
    """Pydantic model for validating the JSON for BP Answers"""

    submission_id: str
    fv_best_practice_id: UUID
    question_key: str
    answer_text: Optional[str]
    answer_numeric: Optional[Decimal]
    answer_boolean: Optional[bool]
    answer_url: Optional[str]
