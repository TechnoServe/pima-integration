from sqlalchemy import Column, String, Integer, Date, Boolean, Numeric, ForeignKey, DateTime, Enum, CheckConstraint, Index
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

class FVBestPractice(Base, AuditMixin, SFIDMixin, SoftDeleteMixin, TimestampMixin, UUIDMixin):
    __tablename__ = "fv_best_practices"
    
    # Indexes and Constraints
    __table_args__ = (
        Index("idx_fv_best_practices_farm_visit_id", "farm_visit_id"),
        Index("idx_fv_best_practices_submission_id", "submission_id"),
        Index("idx_fv_best_practices_sf_id", "sf_id"),
        {'schema': SCHEMA}
    )

    # Columns
    submission_id = Column(String, nullable=False, unique=True)
    farm_visit_id = Column(UUID(as_uuid=True), ForeignKey(f"{SCHEMA}.farm_visits.id"), nullable=False)
    best_practice_type = Column(String, nullable=False)
    is_bp_verified = Column(Boolean, nullable=False, default=False)
    
    # Relationships
    farm_visit = relationship("FarmVisit", back_populates="fv_best_practices")