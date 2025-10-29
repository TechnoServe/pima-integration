import os
from sqlalchemy import (
    Column,
    String,
    Date,
    Boolean,
    Numeric,
    ForeignKey,
    Index,
    Enum,
    text,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from .base import Base
from .mixins import AuditMixin, SoftDeleteMixin, TimestampMixin, UUIDMixin, SFIDMixin
from dotenv import load_dotenv

load_dotenv()

SCHEMA = os.getenv("DB_SCHEMA", "public")


class FarmVisit(
    Base, AuditMixin, SFIDMixin, SoftDeleteMixin, TimestampMixin, UUIDMixin
):
    __tablename__ = "farm_visits"

    # Adding indexes to frequently queried fields
    __table_args__ = (
        Index("idx_farm_visits_visited_household_id", "visited_household_id"),
        Index("idx_farm_visits_visited_primary_farmer_id", "visited_primary_farmer_id"),
        Index(
            "idx_farm_visits_visited_secondary_farmer_id", "visited_secondary_farmer_id"
        ),
        Index("idx_farm_visits_submission_id", "submission_id"),
        Index("idx_farm_visits_training_session_id", "training_session_id"),
        Index("idx_farm_visits_visiting_staff_id", "visiting_staff_id"),
        Index("idx_farm_visits_sf_id", "sf_id"),
        Index("idx_farm_visits_created_by_id", "created_by_id"),
        Index("idx_farm_visits_last_updated_by_id", "last_updated_by_id"),
        {"schema": SCHEMA},
    )

    # Columns
    visited_household_id = Column(
        UUID(as_uuid=True), ForeignKey(f"{SCHEMA}.households.id"), nullable=False
    )
    visited_primary_farmer_id = Column(
        UUID(as_uuid=True), ForeignKey(f"{SCHEMA}.farmers.id"), nullable=False
    )
    visited_secondary_farmer_id = Column(
        UUID(as_uuid=True), ForeignKey(f"{SCHEMA}.farmers.id"), nullable=True
    )
    submission_id = Column(String, nullable=False, unique=True)
    training_session_id = Column(
        UUID(as_uuid=True), ForeignKey(f"{SCHEMA}.training_sessions.id"), nullable=False
    )
    visiting_staff_id = Column(
        UUID(as_uuid=True), ForeignKey(f"{SCHEMA}.users.id"), nullable=False
    )
    date_visited = Column(Date, nullable=False)
    farm_visit_type = Column(
        Enum(
            "Farm Visit Full - ET",
            "Farm Visit Full - KE",
            "Farm Visit Full - PR",
            "Farm Visit Full - ZM",
            name="farm_visit_type_enum",
            schema=SCHEMA
        ),
        nullable=False,
    )
    visit_comments = Column(String, nullable=True)
    latest_visit = Column(
        Boolean, nullable=False, default=True, server_default=text("true")
    )
    location_gps_latitude = Column(Numeric(10, 6), nullable=False)
    location_gps_longitude = Column(Numeric(10, 6), nullable=False)
    location_gps_altitude = Column(Numeric(10, 2), nullable=False)

    # Relationships
    visited_household = relationship("Household", back_populates="farm_visits")
    primary_farmer = relationship(
        "Farmer",
        foreign_keys=[visited_primary_farmer_id],
        back_populates="farm_visits_primary_farmer",
    )
    secondary_farmer = relationship(
        "Farmer",
        foreign_keys=[visited_secondary_farmer_id],
        back_populates="farm_visits_secondary_farmer",
    )
    training_session = relationship("TrainingSession", back_populates="farm_visit")
    visiting_staff = relationship(
        "User", back_populates="farm_visits", foreign_keys=[visiting_staff_id]
    )
    checks = relationship("Check", back_populates="farm_visit")
    fv_best_practices = relationship("FVBestPractice", back_populates="farm_visit")
    farms = relationship("Farm", back_populates="farm_visit")
    # fv_question_answers = relationship("FVQuestionAnswer", back_populates="farm_visit")
