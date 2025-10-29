from sqlalchemy import Column, String, Boolean, Numeric, ForeignKey, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from .base import Base
from .mixins import AuditMixin, SoftDeleteMixin, TimestampMixin, UUIDMixin, SFIDMixin
from dotenv import load_dotenv
import os

load_dotenv()

SCHEMA = os.getenv("DB_SCHEMA", "public")


class ObservationResult(
    Base, AuditMixin, SFIDMixin, SoftDeleteMixin, TimestampMixin, UUIDMixin
):
    __tablename__ = "observation_results"
    __table_args__ = (
        Index("idx_observation_results_observation_id", "observation_id"),
        Index("idx_observation_results_submission_id", "submission_id"),
        Index("idx_observation_results_sf_id", "sf_id"),
        Index("idx_observation_results_created_by_id", "created_by_id"),
        Index("idx_observation_results_last_updated_by_id", "last_updated_by_id"),
        Index("idx_observation_results_question_key", "question_key"),
        {"schema": SCHEMA},
    )

    # Columns
    submission_id = Column(String, nullable=False)
    observation_id = Column(
        UUID(as_uuid=True), ForeignKey(f"{SCHEMA}.observations.id"), nullable=False
    )
    criterion = Column(String, nullable=True)
    question_key = Column(String, nullable=True)
    result_text = Column(String, nullable=True)
    result_numeric = Column(Numeric, nullable=True)
    result_boolean = Column(Boolean, nullable=True)
    result_url = Column(String, nullable=True)

    # Relationships
    observation = relationship("Observation", back_populates="observation_results")
