from typing import Dict, Any
from schemas import ImageCreate
from pydantic import ValidationError
from core.logging_util import logger


class ImageTransformer:
    """Transforms CommCare payload to database-ready schema for images"""

    def __init__(self):
        pass

    def transform(
        self, payload: dict, image_url: str, image_reference_obj: object, image_description: str
    ) -> ImageCreate:
        """Transform CommCare payload to ImageCreate schema"""

        try:

            # Handle different form types and map to appropriate session fields
            session_data = self._map_image(payload, image_url, image_reference_obj, image_description)

            return ImageCreate(**session_data)
        except ValidationError as e:
            logger.error(
                {"message": "Schema validation failed", "errors": str(e.errors())}
            )
            raise ValueError(f"Schema validation failed: {str(e.errors())}") from e

    def _map_image(
        self, payload: dict, image_url: str, image_reference_obj: object, image_description: str
    ) -> Dict[str, Any]:
        """Map data for Image"""

        form_id = payload.get("id")
        submission_id = f"{form_id}{image_reference_obj.id}{image_url.split("/")[-1].split(".")[0]}"

        REFERENCE_OBJ_NAME = {
            "training_sessions": "Training Session",
            "farm_visits": "Farm Visit",
            "farms": "Farm",
            "fv_best_practice_answers": "FV Best Practice Answer",
            "fv_best_practices": "FV Best Practice",
            "observations": "Observation",
            "observation_results": "Observation Result",
        }

        return {
            "submission_id": submission_id,
            "image_reference_type": str(
                REFERENCE_OBJ_NAME.get(image_reference_obj.__tablename__, "Unknown")
            ),
            "image_reference_id": str(image_reference_obj.id),
            "image_description": image_description,
            "image_url": image_url,
            "verification_status": "Pending",
        }
