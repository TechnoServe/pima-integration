from sqlalchemy import Column, String, ForeignKey, Index, Date, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from .base import Base
from .mixins import SoftDeleteMixin, TimestampMixin, UUIDMixin, AuditMixin
import os
from dotenv import load_dotenv

load_dotenv()
SCHEMA = os.getenv("DB_SCHEMA", "public")


class WVSurveyResponse(Base, SoftDeleteMixin, TimestampMixin, UUIDMixin, AuditMixin):
    __tablename__ = "wv_survey_responses"
    __table_args__ = (
        Index("idx_survey_responses_form_visit_id", "form_visit_id"),
        Index("idx_survey_responses_survey_type", "survey_type"),
        Index("idx_survey_responses_submission_id", "submission_id"),
        Index("idx_survey_responses_created_by_id", "created_by_id"),
        Index("idx_survey_responses_last_updated_by_id", "last_updated_by_id"),
        {"schema": SCHEMA},
    )

    # Fields
    form_visit_id = Column(UUID(as_uuid=True), ForeignKey(f"{SCHEMA}.wetmill_visits.id"), nullable=False)
    survey_type = Column(String, nullable=False)
    completed_date = Column(Date, nullable=True)
    general_feedback = Column(Text, nullable=True)
    submission_id = Column(String, nullable=False)

    form_visit = relationship("WetmillVisit", back_populates="surveys")
    question_responses = relationship(
        "WVSurveyQuestionResponse",
        back_populates="survey_response",
        cascade="all, delete-orphan"
    )
