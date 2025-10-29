from uuid import UUID
from pydantic import BaseModel


class CoffeeVarietyCreate(BaseModel):
    """Pydantic model for validating the JSON for FIS Coffee Varieties"""

    variety_name: str
    number_of_trees: int
    submission_id: str
    farm_id: UUID
