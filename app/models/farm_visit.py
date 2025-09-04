from sqlalchemy import Column, String, Integer, Date, Boolean, Numeric, ForeignKey, DateTime, Index, Enum
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

class FarmVisit(Base, AuditMixin, SFIDMixin, SoftDeleteMixin, TimestampMixin, UUIDMixin):
    __tablename__ = "farm_visits"
    
    # Adding indexes to frequently queried fields
    __table_args__ = (
        Index("idx_farm_visits_visited_household_id", "visited_household_id"),
        Index("idx_farm_visits_visited_primary_farmer_id", "visited_primary_farmer_id"),
        Index("idx_farm_visits_visited_secondary_farmer_id", "visited_secondary_farmer_id"),
        Index("idx_farm_visits_submission_id", "submission_id"),
        Index("idx_farm_visits_training_session_id", "training_session_id"),
        Index("idx_farm_visits_visiting_staff_id", "visiting_staff_id"),
        Index("idx_farm_visits_sf_id", "sf_id"),
        {'schema': SCHEMA}
    )

    # Columns
    visited_household_id = Column(UUID(as_uuid=True), ForeignKey(f"{SCHEMA}.households.id"), nullable=False)
    visited_primary_farmer_id = Column(UUID(as_uuid=True), ForeignKey(f"{SCHEMA}.farmers.id"), nullable=False)
    visited_secondary_farmer_id = Column(UUID(as_uuid=True), ForeignKey(f"{SCHEMA}.farmers.id"), nullable=True)
    submission_id = Column(String, nullable=False, unique=True)
    training_session_id = Column(UUID(as_uuid=True), ForeignKey(f"{SCHEMA}.training_sessions.id"), nullable=False)
    visiting_staff_id = Column(UUID(as_uuid=True), ForeignKey(f"{SCHEMA}.staff.id"), nullable=False)
    date_visited = Column(Date, nullable=False)
    farm_visit_type = Column(Enum("Farm Visit Full - ET", "Farm Visit Full - KE", "Farm Visit Full - PR", "Farm Visit Full - ZM", name="farm_visit_type_enum"), nullable=False)
    visit_comments = Column(String, nullable=True)
    latest_visit = Column(Boolean, nullable=False, default=True)
    location_gps_latitude = Column(Numeric(10, 6), nullable=False)
    location_gps_longitude = Column(Numeric(10, 6), nullable=False)
    location_gps_altitude = Column(Numeric(10, 2), nullable=False)
    number_of_cuerdas = Column(Integer, nullable=True)
    number_of_separate_coffee_fields = Column(Integer, nullable=True)
    field_age = Column(Numeric, nullable=True)
    field_size = Column(Numeric(10, 2), nullable=True)
    
    # Relationships
    visited_household = relationship("Household", back_populates="farm_visits")
    primary_farmer = relationship("Farmer", foreign_keys=[visited_primary_farmer_id], back_populates="farm_visits")
    secondary_farmer = relationship("Farmer", foreign_keys=[visited_secondary_farmer_id], back_populates="farm_visits")
    training_session = relationship("TrainingSession", back_populates="farm_visit")
    visiting_staff = relationship("Staff", back_populates="farm_visits")
    checks = relationship("Check", back_populates="farm_visit")
    fv_best_practices = relationship("FVBestPractice", back_populates="farm_visit")