from typing import Literal
from uuid import UUID
from pydantic import BaseModel


class FVBestPracticeCreate(BaseModel):
    submission_id: str
    farm_visit_id: UUID
    best_practice_type: Literal[
        "Stumping",
        "Nutrition",
        "Weeding",
        "Integrated Pest & Disease Management",
        "Erosion Control",
        "Shade Management",
        "Compost",
        "Main Stems",
        "Pruning",
        "Pesticide Use",
        "Record Keeping",
        "Health of New Planting",
        "Other FV Questions"
    ]
    is_bp_verified: bool
