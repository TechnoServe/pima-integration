from sqlalchemy import Column, String, ForeignKey, Index, Text, Float, Boolean, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from geoalchemy2 import Geometry
from .base import Base
from .mixins import SoftDeleteMixin, TimestampMixin, UUIDMixin, AuditMixin
import os
from dotenv import load_dotenv

load_dotenv()
SCHEMA = os.getenv("DB_SCHEMA", "public")


class WVSurveyQuestionResponse(Base, SoftDeleteMixin, TimestampMixin, UUIDMixin, AuditMixin):
    __tablename__ = "wv_survey_question_responses"
    __table_args__ = (
        Index("idx_survey_question_responses_survey_response_id", "survey_response_id"),
        Index("idx_survey_question_responses_question_name", "question_name"),
        Index("idx_survey_question_responses_submission_id", "submission_id"),
        Index("idx_survey_question_responses_created_by_id", "created_by_id"),
        Index("idx_survey_question_responses_last_updated_by_id", "last_updated_by_id"),
        {"schema": SCHEMA},
    )

    # Fields
    survey_response_id = Column(
        UUID(as_uuid=True), ForeignKey(f"{SCHEMA}.wv_survey_responses.id"), nullable=False
    )
    section_name = Column(String, nullable=True)
    question_name = Column(String, nullable=False)
    field_type = Column(String, nullable=False)
    submission_id = Column(String, nullable=False)

    value_text = Column(Text, nullable=True)
    value_number = Column(Float, nullable=True)
    value_boolean = Column(Boolean, nullable=True)
    value_date = Column(DateTime, nullable=True)
    value_gps = Column(Geometry("POINT", srid=4326, spatial_index=False), nullable=True)

    survey_response = relationship(
        "WVSurveyResponse", back_populates="question_responses"
    )
