from sqlalchemy import Column, String, Integer, Date, Boolean, Numeric, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID
from .base import Base
from .mixins.audit import AuditMixin
from .mixins.soft_delete import SoftDeleteMixin
from .mixins.timestamp import TimestampMixin
from .mixins.uuid import UUIDMixin
from dotenv import load_dotenv
import os
load_dotenv()

SCHEMA = os.getenv("DB_SCHEMA", "public")

class Image(Base, AuditMixin, SoftDeleteMixin, TimestampMixin, UUIDMixin):
    __tablename__ = "images"
    __table_args__ = {'schema': SCHEMA}
    
    # Columns
    image_reference_type = Column(String, nullable=True)
    image_reference_id = Column(UUID(as_uuid=True))
    image_url = Column(String, nullable=True)
    verification_status = Column(String, nullable=True)