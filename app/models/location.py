from sqlalchemy import Column, String, Integer, Date, Boolean, Numeric, ForeignKey, DateTime, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from .base import Base
from .mixins.audit import AuditMixin
from .mixins.sf_id import SFIDMixin
from .mixins.soft_delete import SoftDeleteMixin
from .mixins.timestamp import TimestampMixin
from .mixins.uuid import UUIDMixin
from dotenv import load_dotenv
import os
load_dotenv()

SCHEMA = os.getenv("DB_SCHEMA", "public")

class Location(Base, AuditMixin, SFIDMixin, SoftDeleteMixin, TimestampMixin, UUIDMixin):
    __tablename__ = "locations"
    __table_args__ = (
        Index("idx_locations_parent_location_id", "parent_location_id"),
        {'schema': SCHEMA}
    )

    # Columns
    location_name = Column(String, nullable=False)
    location_type = Column(String, nullable=False)
    parent_location_id = Column(UUID(as_uuid=True), ForeignKey(f"{SCHEMA}.locations.id"), nullable=True)
    
    # Relationships
    parent_location = relationship("Location", remote_side="Location.id", back_populates="child_locations")
    child_locations = relationship("Location", back_populates="parent_location", cascade="all, delete-orphan")
