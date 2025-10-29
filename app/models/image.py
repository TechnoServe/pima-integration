from sqlalchemy import Column, String, Index
from sqlalchemy.dialects.postgresql import UUID
from .base import Base
from .mixins import AuditMixin, SoftDeleteMixin, TimestampMixin, UUIDMixin
from dotenv import load_dotenv
import os

load_dotenv()

SCHEMA = os.getenv("DB_SCHEMA", "public")


class Image(Base, AuditMixin, SoftDeleteMixin, TimestampMixin, UUIDMixin):
    __tablename__ = "images"
    __table_args__ = (
        Index("idx_images_image_reference_id", "image_reference_id"),
        Index("idx_images_created_by_id", "created_by_id"),
        Index("idx_images_last_updated_by_id", "last_updated_by_id"),
        Index("idx_images_submission_id", "submission_id"),
        {"schema": SCHEMA},
    )

    # Columns
    image_reference_type = Column(String, nullable=True)
    image_reference_id = Column(UUID(as_uuid=True))
    image_url = Column(String, nullable=True)
    image_description = Column(String, nullable=True)
    submission_id = Column(String, nullable=False)
    verification_status = Column(String, nullable=True)
