from sqlalchemy import Column, String, ForeignKey, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from .base import Base
from .mixins import AuditMixin, SoftDeleteMixin, TimestampMixin, UUIDMixin, SFIDMixin
from dotenv import load_dotenv
import os

load_dotenv()

SCHEMA = os.getenv("DB_SCHEMA", "public")


class Location(Base, AuditMixin, SFIDMixin, SoftDeleteMixin, TimestampMixin, UUIDMixin):
    __tablename__ = "locations"
    __table_args__ = (
        Index("idx_locations_parent_location_id", "parent_location_id"),
        Index("idx_locations_sf_id", "sf_id"),
        Index("idx_locations_created_by_id", "created_by_id"),
        Index("idx_locations_last_updated_by_id", "last_updated_by_id"),
        {"schema": SCHEMA},
    )

    # Columns
    location_name = Column(String, nullable=False)
    location_type = Column(String, nullable=False)
    parent_location_id = Column(
        UUID(as_uuid=True), ForeignKey(f"{SCHEMA}.locations.id"), nullable=True
    )

    # Relationships
    parent_location = relationship(
        "Location", remote_side="Location.id", back_populates="child_locations"
    )
    child_locations = relationship(
        "Location", back_populates="parent_location", cascade="all, delete-orphan"
    )
    farmer_groups = relationship("FarmerGroup", back_populates="location")
    projects = relationship("Project", back_populates="location")
