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

class FVBestPracticeAnswer(Base, AuditMixin, SFIDMixin, SoftDeleteMixin, TimestampMixin, UUIDMixin):
    __tablename__ = "fv_best_practice_answers"
    
    # Indexes and Constraints
    __table_args__ = (
        Index("idx_fv_best_practice_answers_fv_best_practice_id", "fv_best_practice_id"),
        Index("idx_fv_best_practice_answers_submission_id", "submission_id"),
        {'schema': SCHEMA}
    )

    # Columns
    submission_id = Column(String, nullable=False, unique=True)
    fv_best_practice_id = Column(UUID(as_uuid=True), ForeignKey(f"{SCHEMA}.fv_best_practices.id"), nullable=False)
    question_key = Column(String, nullable=False)
    answer_text = Column(String, nullable=True)
    answer_numeric = Column(Numeric, nullable=True)
    answer_boolean = Column(Boolean, nullable=True)
    answer_url = Column(String, nullable=True)
    
    # Relationships
    fv_best_practice = relationship("FVBestPractice", back_populates="fv_best_practice_answers")