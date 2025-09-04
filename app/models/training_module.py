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

class TrainingModule(Base, AuditMixin, SoftDeleteMixin, SFIDMixin, TimestampMixin, UUIDMixin):
    __tablename__ = "training_modules"
    __table_args__ = {'schema': os.getenv("DB_SCHEMA", "public")}
    
    # Columns
    project_id = Column(UUID(as_uuid=True), ForeignKey(f"{SCHEMA}.projects.id"), nullable=True)
    module_name = Column(String, nullable=True)
    module_number = Column(Integer, nullable=True)
    current_module = Column(Boolean, default=False)
    current_previous = Column(Enum("Current", "Previous", name="current_previous_enum"), nullable=False)
    sample_fv_aa_households = Column(Boolean, default=False)
    sample_fv_aa_households_status = Column(String, nullable=True)
    
    # Relationships
    project = relationship("Project", back_populates="training_modules")
    training_sessions = relationship("TrainingSession", back_populates="training_module")    