from sqlalchemy import Column, String, Boolean, Numeric, ForeignKey, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from .base import Base
from .mixins import AuditMixin, SoftDeleteMixin, TimestampMixin, UUIDMixin, SFIDMixin
from dotenv import load_dotenv
import os

load_dotenv()

SCHEMA = os.getenv("DB_SCHEMA", "public")


class FVBestPracticeAnswer(
    Base, AuditMixin, SFIDMixin, SoftDeleteMixin, TimestampMixin, UUIDMixin
):
    __tablename__ = "fv_best_practice_answers"

    # Indexes and Constraints
    __table_args__ = (
        Index(
            "idx_fv_best_practice_answers_fv_best_practice_id", "fv_best_practice_id"
        ),
        Index("idx_fv_best_practice_answers_submission_id", "submission_id"),
        Index("idx_fv_best_practice_answers_sf_id", "sf_id"),
        Index("idx_fv_best_practice_answers_created_by_id", "created_by_id"),
        Index("idx_fv_best_practice_answers_last_updated_by_id", "last_updated_by_id"),
        Index("idx_fv_best_practice_answers_question_key", "question_key"),
        {"schema": SCHEMA},
    )

    # Columns
    submission_id = Column(String, nullable=False, unique=True)
    fv_best_practice_id = Column(
        UUID(as_uuid=True), ForeignKey(f"{SCHEMA}.fv_best_practices.id"), nullable=False
    )
    question_key = Column(String, nullable=False)
    answer_text = Column(String, nullable=True)
    answer_numeric = Column(Numeric, nullable=True)
    answer_boolean = Column(Boolean, nullable=True)
    answer_url = Column(String, nullable=True)

    # Relationships
    fv_best_practice = relationship(
        "FVBestPractice", back_populates="fv_best_practice_answers"
    )
