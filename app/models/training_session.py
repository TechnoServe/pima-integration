from sqlalchemy import (
    Column,
    String,
    Integer,
    Date,
    Boolean,
    Numeric,
    ForeignKey,
    Enum,
    text,
    Index,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from .base import Base
from .mixins import AuditMixin, SoftDeleteMixin, TimestampMixin, UUIDMixin, SFIDMixin
from dotenv import load_dotenv
import os

load_dotenv()

SCHEMA = os.getenv("DB_SCHEMA", "public")


class TrainingSession(
    Base, AuditMixin, SoftDeleteMixin, TimestampMixin, UUIDMixin, SFIDMixin
):
    __tablename__ = "training_sessions"
    __table_args__ = (
        Index("idx_training_sessions_trainer_id", "trainer_id"),
        Index("idx_training_sessions_module_id", "module_id"),
        Index("idx_training_sessions_farmer_group_id", "farmer_group_id"),
        Index("idx_training_sessions_commcare_case_id", "commcare_case_id"),
        Index("idx_training_sessions_created_by_id", "created_by_id"),
        Index("idx_training_sessions_last_updated_by_id", "last_updated_by_id"),
        {"schema": SCHEMA},
    )

    trainer_id = Column(
        UUID(as_uuid=True), ForeignKey(f"{SCHEMA}.users.id"), nullable=True
    )
    module_id = Column(
        UUID(as_uuid=True), ForeignKey(f"{SCHEMA}.training_modules.id"), nullable=False
    )
    farmer_group_id = Column(
        UUID(as_uuid=True), ForeignKey(f"{SCHEMA}.farmer_groups.id"), nullable=False
    )

    date_session_1 = Column(Date, nullable=True)
    date_session_2 = Column(Date, nullable=True)
    commcare_case_id = Column(String, unique=True, nullable=False)

    male_attendees_session_1 = Column(Integer, nullable=True)
    female_attendees_session_1 = Column(Integer, nullable=True)
    total_attendees_session_1 = Column(Integer, nullable=True)

    male_attendees_session_2 = Column(Integer, nullable=True)
    female_attendees_session_2 = Column(Integer, nullable=True)
    total_attendees_session_2 = Column(Integer, nullable=True)

    male_attendees_agg = Column(Integer, nullable=True)
    female_attendees_agg = Column(Integer, nullable=True)
    total_attendees_agg = Column(Integer, nullable=True)

    location_gps_latitude_session_1 = Column(Numeric(10, 6))
    location_gps_longitude_session_1 = Column(Numeric(10, 6))
    location_gps_altitude_session_1 = Column(Numeric(10, 2))

    location_gps_latitude_session_2 = Column(Numeric(10, 6))
    location_gps_longitude_session_2 = Column(Numeric(10, 6))
    location_gps_altitude_session_2 = Column(Numeric(10, 2))

    send_to_commcare = Column(
        Boolean, default=False, server_default=text("false"), nullable=False
    )
    send_to_commcare_status = Column(
        Enum(
            "Pending",
            "Processing",
            "Complete",
            name="training_session_send_to_commcare_status_enum",
            schema=SCHEMA
        ),
        nullable=False,
        default="Pending",
        server_default="Pending",
    )

    # Relationships
    trainer = relationship(
        "User", back_populates="training_sessions", foreign_keys=[trainer_id]
    )
    training_module = relationship("TrainingModule", back_populates="training_sessions")
    farmer_group = relationship("FarmerGroup", back_populates="training_sessions")
    farm_visit = relationship("FarmVisit", back_populates="training_session")
    checks = relationship("Check", back_populates="training_session")
    observation = relationship("Observation", back_populates="training_session")
    attendances = relationship("Attendance", back_populates="training_session")
