from sqlalchemy.orm import Session
from models import Image
from schemas import ImageCreate
from core import logger


class ImageService:
    """Handles database operations for images"""

    def __init__(self, db: Session):
        self.db = db

    def upsert(self, data: ImageCreate, created_by_id: str) -> Image:
        """Upsert image data"""

        # Check if record exists by CommCare case ID
        existing = (
            self.db.query(Image)
            .filter(
                Image.submission_id == data.submission_id, Image.is_deleted == False
            )
            .first()
        )

        if existing:
            logger.info(
                {"message": f"Updating existing image record: {data.submission_id}"}
            )
            return self._update_existing(existing, data, created_by_id)
        else:
            logger.info({"message": f"Creating new image record: {data.submission_id}"})
            return self._create_new(data, created_by_id)

    def _update_existing(
        self, existing: Image, data: ImageCreate, updated_by_id: str
    ) -> Image:
        """Update existing image with smart merging"""

        # Smart update: don't overwrite existing data with None values
        for field, value in data.model_dump(exclude_unset=True).items():
            if field in ["training_session_id", "farmer_id", "submission_id"]:
                # Always update core fields
                setattr(existing, field, value)
            elif value is not None:
                # Only update other fields if new value is not None
                current_value = getattr(existing, field, None)
                if current_value is None or value != current_value:
                    setattr(existing, field, value)

        existing.last_updated_by_id = updated_by_id

        self.db.commit()
        self.db.refresh(existing)
        return existing

    def _create_new(self, data: ImageCreate, created_by_id: str) -> Image:
        """Create new image"""

        # print(data)

        attendance = Image(
            **data.model_dump(exclude_unset=True),
            created_by_id=created_by_id,
            last_updated_by_id=created_by_id,
        )

        self.db.add(attendance)
        self.db.commit()
        self.db.refresh(attendance)
        return attendance
