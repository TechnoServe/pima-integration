from sqlalchemy import Column, String, Integer, Date, Boolean, Numeric, ForeignKey, DateTime, Index, CheckConstraint
from sqlalchemy.dialects.postgresql import UUID, ENUM
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

class Attendance(Base, AuditMixin, SoftDeleteMixin, TimestampMixin, UUIDMixin, SFIDMixin):
    __tablename__ = "attendances"
    
    # Indexes and Table Arguments
    __table_args__ = (
        Index("idx_attendances_farmer_id", "farmer_id"),
        Index("idx_attendances_training_session_id", "training_session_id"),
        Index("idx_attendances_submission_id", "submission_id"),
        Index("idx_attendances_sf_id", "sf_id"),
        CheckConstraint("date_attended <= CURRENT_DATE", name="chk_date_attended_not_future"),
        {'schema': SCHEMA}
    )

    # Columns
    farmer_id = Column(UUID(as_uuid=True), ForeignKey(f"{SCHEMA}.farmers.id"), nullable=False)
    training_session_id = Column(UUID(as_uuid=True), ForeignKey(f"{SCHEMA}.training_sessions.id"), nullable=False)
    date_attended = Column(Date, nullable=False)
    status = Column(ENUM('Present', 'Absent', name='attendance_status_enum'), nullable=False)
    submission_id = Column(String, nullable=False, unique=True)
    
    # Relationships
    farmer = relationship("Farmer", back_populates="attendances")
    training_session = relationship("TrainingSession", back_populates="attendances")
    
    
    