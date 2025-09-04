from sqlalchemy import Column, String, Integer, Date, Boolean, Numeric, ForeignKey, DateTime, Index, CheckConstraint, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from .base import Base
from .mixins.audit import AuditMixin
from .mixins.soft_delete import SoftDeleteMixin
from .mixins.timestamp import TimestampMixin
from .mixins.uuid import UUIDMixin
from .mixins.sf_id import SFIDMixin
from dotenv import load_dotenv
import os
load_dotenv()

SCHEMA = os.getenv("DB_SCHEMA", "public")

class Check(Base, AuditMixin, SoftDeleteMixin, TimestampMixin, UUIDMixin, SFIDMixin):
    __tablename__ = "checks"
    __table_args__ = (
        Index("idx_checks_farmer_id", "farmer_id"),
        Index("idx_checks_submission_id", "submission_id"),
        Index("idx_checks_checker_id", "checker_id"),
        Index("idx_checks_training_session_id", "training_session_id"),
        Index("idx_checks_farm_visit_id", "farm_visit_id"),
        Index("idx_checks_observation_id", "observation_id"),
        Index("idx_checks_sf_id", "sf_id"),
        CheckConstraint("date_completed <= CURRENT_DATE", name="chk_date_completed_not_future"),
        CheckConstraint("number_of_trainings_attended <= 50 AND number_of_trainings_attended >= 0", name="chk_number_of_trainings_attended_valid"),
        {'schema': SCHEMA}
    )

    farmer_id = Column(UUID(as_uuid=True), ForeignKey(f"{SCHEMA}.farmers.id"), nullable=False)
    submission_id = Column(String, nullable=False, unique=True)
    checker_id = Column(UUID(as_uuid=True), ForeignKey(f"{SCHEMA}.staff.id"), nullable=False)
    observation_id = Column(UUID(as_uuid=True), ForeignKey(f"{SCHEMA}.observations.id"), nullable=True)
    farm_visit_id = Column(UUID(as_uuid=True), ForeignKey(f"{SCHEMA}.farm_visits.id"), nullable=True)
    training_session_id = Column(UUID(as_uuid = True), ForeignKey(f"{SCHEMA}.training_sessions.id"), nullable=False)
    check_type = Column(Enum('Training Observation', 'Farm Visit', name='check_type_enum'), nullable=False)
    date_completed = Column(Date, nullable=False)
    attended_trainings = Column(Boolean, nullable=True)
    number_of_trainings_attended = Column(Integer, nullable=True)
    attended_last_months_training = Column(Boolean, nullable=False)
    
    # Relationships
    farmer = relationship("Farmer", back_populates="checks")
    checker = relationship("Staff", back_populates="checks")
    observation = relationship("Observation", back_populates="checks")
    farm_visit = relationship("FarmVisit", back_populates="checks")
    training_session = relationship("TrainingSession", back_populates="checks")
    
    