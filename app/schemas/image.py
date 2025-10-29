import uuid
from typing import Optional
from pydantic import BaseModel


class ImageCreate(BaseModel):
    submission_id: str
    image_reference_type: str
    image_reference_id: uuid.UUID
    image_description: Optional[str]
    image_url: str
    verification_status: str

    model_config = {
        "from_attributes": True,
    }
