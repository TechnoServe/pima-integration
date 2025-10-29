from sqlalchemy import (
    Column,
    String,
    Integer,
    Boolean,
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


class TrainingModule(
    Base, AuditMixin, SoftDeleteMixin, SFIDMixin, TimestampMixin, UUIDMixin
):
    __tablename__ = "training_modules"
    __table_args__ = (
        Index("idx_training_modules_project_id", "project_id"),
        Index("idx_training_modules_sf_id", "sf_id"),
        Index("idx_training_modules_created_by_id", "created_by_id"),
        Index("idx_training_modules_last_updated_by_id", "last_updated_by_id"),
        {"schema": SCHEMA},
    )

    # Columns
    project_id = Column(
        UUID(as_uuid=True), ForeignKey(f"{SCHEMA}.projects.id"), nullable=True
    )
    module_name = Column(String, nullable=True)
    module_number = Column(Integer, nullable=True)
    current_module = Column(Boolean, default=False, server_default=text("false"))
    current_previous = Column(
        Enum("Current", "Previous", name="current_previous_enum", schema=SCHEMA), nullable=False
    )
    sample_fv_aa_households = Column(
        Boolean, default=False, server_default=text("false")
    )
    sample_fv_aa_households_status = Column(String, nullable=True)
    status = Column(
        Enum("Active", "Inactive", name="training_module_status_enum", schema=SCHEMA),
        nullable=False,
        default="Active",
        server_default="Active",
    )

    # Relationships
    project = relationship("Project", back_populates="training_modules")
    training_sessions = relationship(
        "TrainingSession", back_populates="training_module"
    )
