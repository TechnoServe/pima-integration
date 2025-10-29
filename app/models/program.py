from sqlalchemy import Column, String, Index
from sqlalchemy.orm import relationship
from .base import Base
from .mixins import AuditMixin, SoftDeleteMixin, TimestampMixin, UUIDMixin, SFIDMixin
from dotenv import load_dotenv
import os

load_dotenv()

SCHEMA = os.getenv("DB_SCHEMA", "public")


class Program(Base, AuditMixin, TimestampMixin, SoftDeleteMixin, SFIDMixin, UUIDMixin):
    __tablename__ = "programs"
    __table_args__ = (
        Index("idx_programs_sf_id", "sf_id"),
        Index("idx_programs_created_by_id", "created_by_id"),
        Index("idx_programs_last_updated_by_id", "last_updated_by_id"),
        {"schema": SCHEMA},
    )

    # Columns
    program_name = Column(String, nullable=False)
    program_code = Column(String, nullable=False, unique=True)

    # Relationships
    projects = relationship("Project", back_populates="program")
