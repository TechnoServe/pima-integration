from sqlalchemy import Column, String, Boolean, ForeignKey, Index, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from .base import Base
from .mixins import AuditMixin, SoftDeleteMixin, TimestampMixin, UUIDMixin, SFIDMixin
from dotenv import load_dotenv
import os

load_dotenv()

SCHEMA = os.getenv("DB_SCHEMA", "public")


class FVBestPractice(
    Base, AuditMixin, SFIDMixin, SoftDeleteMixin, TimestampMixin, UUIDMixin
):
    __tablename__ = "fv_best_practices"

    # Indexes and Constraints
    __table_args__ = (
        Index("idx_fv_best_practices_farm_visit_id", "farm_visit_id"),
        Index("idx_fv_best_practices_submission_id", "submission_id"),
        Index("idx_fv_best_practices_sf_id", "sf_id"),
        Index("idx_fv_best_practices_created_by_id", "created_by_id"),
        Index("idx_fv_best_practices_last_updated_by_id", "last_updated_by_id"),
        {"schema": SCHEMA},
    )

    # Columns
    submission_id = Column(String, nullable=False, unique=True)
    farm_visit_id = Column(
        UUID(as_uuid=True), ForeignKey(f"{SCHEMA}.farm_visits.id"), nullable=False
    )
    best_practice_type = Column(String, nullable=False)
    is_bp_verified = Column(
        Boolean, nullable=False, default=False, server_default=text("false")
    )

    # Relationships
    farm_visit = relationship("FarmVisit", back_populates="fv_best_practices")
    fv_best_practice_answers = relationship(
        "FVBestPracticeAnswer", back_populates="fv_best_practice"
    )
