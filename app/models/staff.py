from sqlalchemy import Column, String, Integer, Date, Boolean, Numeric, ForeignKey, Enum
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

class Staff(Base, AuditMixin, SFIDMixin, SoftDeleteMixin, TimestampMixin, UUIDMixin):
    __tablename__ = "staff"
    __table_args__ = {'schema': SCHEMA}
    
    first_name = Column(String, nullable=True)
    middle_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    manager_id = Column(UUID(as_uuid=True), ForeignKey(f"{SCHEMA}.staff.id"), nullable=True)
    tns_id = Column(String, unique=True, index=True, nullable=True)
    commcare_mobile_worker_id = Column(String, unique=True, index=True, nullable=True)
    email = Column(String, unique=True, index=True, nullable=True)
    password = Column(String, nullable=True)
    phone_number = Column(String, nullable=True)
    job_title = Column(String, nullable=True)
    status = Column(Enum("Active", "Inactive", name="status_enum"), nullable=True)
    
    # Relationships
    project_staff_roles = relationship("ProjectStaffRole", back_populates="staff")
    manager = relationship("Staff", remote_side="Staff.id", back_populates="subordinates")
    subordinates = relationship("Staff", back_populates="manager", cascade="all, delete-orphan")
    farmer_groups = relationship("FarmerGroup", back_populates="responsible_staff")
    training_sessions = relationship("TrainingSession", back_populates="trainer")
    observer_observations = relationship("Observation", back_populates="observer", foreign_keys="Observation.observer_id")
    trainer_observations = relationship("Observation", back_populates="trainer", foreign_keys="Observation.trainer_id")
    farm_visits = relationship("FarmVisit", back_populates="visiting_staff")
    checks = relationship("Check", back_populates="checker")