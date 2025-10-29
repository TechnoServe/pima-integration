from typing import Literal, Optional
from uuid import UUID
from pydantic import BaseModel


class ObservationResultCreate(BaseModel):
    submission_id: str
    observation_id: UUID
    criterion: Literal[
        "Participant Feedback",
        "Observer Feedback",
        "Compost Heap",
        "Mulch",
        "Shade Management",
        "Vetiver Planted",
        "Weed Management",
        "Rejuvenation",
        "Sucker Selection",
        "Stumped Trees",
        "Covercrop Planted",
        "Pruning"
    ]
    question_key: str
    result_text: Optional[str] = None
    result_numeric: Optional[float] = None
    result_boolean: Optional[bool] = None
    result_url: Optional[str] = None
