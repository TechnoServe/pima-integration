from sqlalchemy import Column, String, Integer, Date, Boolean, Numeric, ForeignKey, DateTime, Enum
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

class TrainingSession(Base, AuditMixin, SoftDeleteMixin, TimestampMixin, UUIDMixin, SFIDMixin):
    __tablename__ = "training_sessions"
    __table_args__ = {'schema': os.getenv("DB_SCHEMA", "public")}

    trainer_id = Column(UUID(as_uuid=True), ForeignKey(f"{SCHEMA}.staff.id"), nullable=True)
    module_id = Column(UUID(as_uuid=True), ForeignKey(f"{SCHEMA}.training_modules.id"), nullable=True)
    farmer_group_id = Column(UUID(as_uuid=True), ForeignKey(f"{SCHEMA}.farmer_groups.id"), nullable=True)

    date_session_1 = Column(Date, nullable=True)
    date_session_2 = Column(Date, nullable=True)
    commcare_case_id = Column(String, unique=True, index=True)

    male_attendees_session_1 = Column(Integer, default=0)
    female_attendees_session_1 = Column(Integer, default=0)
    total_attendees_session_1 = Column(Integer, default=0)
    
    male_attendees_session_2 = Column(Integer, default=0)
    female_attendees_session_2 = Column(Integer, default=0)
    total_attendees_session_2 = Column(Integer, default=0)
    
    male_attendees_agg = Column(Integer, default=0)
    female_attendees_agg = Column(Integer, default=0)
    total_attendees_agg = Column(Integer, default=0)

    location_gps_latitude_session_1 = Column(Numeric(10, 6))
    location_gps_longitude_session_1 = Column(Numeric(10, 6))
    location_gps_altitude_session_1 = Column(Numeric(10, 2))
    
    location_gps_latitude_session_2 = Column(Numeric(10, 6))
    location_gps_longitude_session_2 = Column(Numeric(10, 6))
    location_gps_altitude_session_2 = Column(Numeric(10, 2))

    send_to_commcare = Column(Boolean, default=False)
    send_to_commcare_status = Column(Enum("Pending", "Processing", "Complete", name="send_to_commcare_status_enum"), nullable=False, default="Pending")
    
    # Relationships
    trainer = relationship("Staff", back_populates="training_sessions")
    training_module = relationship("TrainingModule", back_populates="training_sessions")
    farmer_group = relationship("FarmerGroup", back_populates="training_sessions")
    attendance = relationship("Attendance", back_populates="training_session")
    farm_visit = relationship("FarmVisit", back_populates="training_session")
    checks = relationship("Check", back_populates="training_session")
    observation = relationship("Observation", back_populates="training_session")
    attendances = relationship("Attendance", back_populates="training_session")
