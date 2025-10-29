from sqlalchemy import Column, String, Integer, Date, Numeric, ForeignKey, Index, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from .base import Base
from .mixins import AuditMixin, SoftDeleteMixin, TimestampMixin, UUIDMixin, SFIDMixin
from dotenv import load_dotenv
import os

load_dotenv()

SCHEMA = os.getenv("DB_SCHEMA", "public")


class Observation(
    Base, AuditMixin, TimestampMixin, SFIDMixin, SoftDeleteMixin, UUIDMixin
):
    __tablename__ = "observations"
    __table_args__ = (
        Index("idx_observations_submission_id", "submission_id"),
        Index("idx_observations_observer_id", "observer_id"),
        Index("idx_observations_trainer_id", "trainer_id"),
        Index("idx_observations_farmer_group_id", "farmer_group_id"),
        Index("idx_observations_training_session_id", "training_session_id"),
        Index("idx_observations_sf_id", "sf_id"),
        Index("idx_observations_created_by_id", "created_by_id"),
        Index("idx_observations_last_updated_by_id", "last_updated_by_id"),
        {"schema": SCHEMA},
    )

    # Columns
    submission_id = Column(String, nullable=False)
    observation_type = Column(
        Enum("Training", "Demo Plot", name="observation_type_enum", schema=SCHEMA), nullable=False
    )
    observer_id = Column(
        UUID(as_uuid=True), ForeignKey(f"{SCHEMA}.users.id"), nullable=False
    )
    trainer_id = Column(
        UUID(as_uuid=True), ForeignKey(f"{SCHEMA}.users.id"), nullable=True
    )
    farmer_group_id = Column(
        UUID(as_uuid=True), ForeignKey(f"{SCHEMA}.farmer_groups.id"), nullable=False
    )
    training_session_id = Column(
        UUID(as_uuid=True), ForeignKey(f"{SCHEMA}.training_sessions.id"), nullable=True
    )

    observation_date = Column(Date, nullable=False)
    location_gps_latitude = Column(Numeric(10, 6), nullable=False)
    location_gps_longitude = Column(Numeric(10, 6), nullable=False)
    location_gps_altitude = Column(Numeric(10, 2), nullable=False)
    female_attendees = Column(Integer, nullable=True)
    male_attendees = Column(Integer, nullable=True)
    total_attendees = Column(Integer, nullable=True)
    comments = Column(String, nullable=True)

    # Relationships
    observation_results = relationship(
        "ObservationResult", back_populates="observation", cascade="all, delete-orphan"
    )
    observer = relationship(
        "User", back_populates="observer_observations", foreign_keys=[observer_id]
    )
    trainer = relationship(
        "User", back_populates="trainer_observations", foreign_keys=[trainer_id]
    )
    farmer_group = relationship("FarmerGroup", back_populates="observations")
    training_session = relationship("TrainingSession", back_populates="observation")
    checks = relationship("Check", back_populates="observation")
