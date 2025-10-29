from sqlalchemy import Column, String, Date, ForeignKey, Enum, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from .base import Base
from .mixins import AuditMixin, SoftDeleteMixin, TimestampMixin, UUIDMixin, SFIDMixin
from dotenv import load_dotenv
import os

load_dotenv()


SCHEMA = os.getenv("DB_SCHEMA", "public")


class Project(Base, AuditMixin, SoftDeleteMixin, SFIDMixin, TimestampMixin, UUIDMixin):
    __tablename__ = "projects"
    __table_args__ = (
        Index("idx_projects_program_id", "program_id"),
        Index("idx_projects_project_unique_id", "project_unique_id"),
        Index("idx_projects_location_id", "location_id"),
        Index("idx_projects_created_by_id", "created_by_id"),
        Index("idx_projects_last_updated_by_id", "last_updated_by_id"),
        {"schema": SCHEMA},
    )

    program_id = Column(
        UUID(as_uuid=True), ForeignKey(f"{SCHEMA}.programs.id"), nullable=True
    )
    project_name = Column(String, nullable=False)
    project_unique_id = Column(String, unique=True, nullable=False)
    status = Column(
        Enum("Active", "Inactive", name="project_status_enum", schema=SCHEMA),
        nullable=False,
        default="Active",
        server_default="Active",
    )
    location_id = Column(
        UUID(as_uuid=True), ForeignKey(f"{SCHEMA}.locations.id"), nullable=True
    )
    start_date = Column(Date, nullable=True)
    end_date = Column(Date, nullable=True)

    # Relationships
    farmer_groups = relationship("FarmerGroup", back_populates="project")
    project_staff_roles = relationship("ProjectStaffRole", back_populates="project")
    location = relationship("Location", back_populates="projects")
    program = relationship("Program", back_populates="projects")
    training_modules = relationship("TrainingModule", back_populates="project")
