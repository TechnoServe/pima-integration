from sqlalchemy import Column, String, Integer, Date, Boolean, Numeric, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
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

class Project(Base, AuditMixin, SoftDeleteMixin, SFIDMixin, TimestampMixin, UUIDMixin):
    __tablename__ = "projects"
    __table_args__ = {'schema': os.getenv("DB_SCHEMA", "public")}

    program_id = Column(UUID(as_uuid=True), ForeignKey(f"{SCHEMA}.programs.id"), nullable=True)
    project_name = Column(String, nullable=False)
    project_unique_id = Column(String, unique=True, nullable=False)
    status = Column(String, nullable=False)
    location_id = Column(UUID(as_uuid=True), ForeignKey(f"{SCHEMA}.locations.id"), nullable=True)
    start_date = Column(Date, nullable=True)
    end_date = Column(Date, nullable=True)
    
    # Relationships
    farmer_groups = relationship("FarmerGroup", back_populates="project")
    project_staff_roles = relationship("ProjectStaffRole", back_populates="project")
    location = relationship("Location", back_populates="projects")
    program = relationship("Program", back_populates="projects")
    training_modules = relationship("TrainingModule", back_populates="project")