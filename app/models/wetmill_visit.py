from sqlalchemy import Column, String, ForeignKey, Index, Date
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from geoalchemy2 import Geometry
from .base import Base
from .mixins import SoftDeleteMixin, TimestampMixin, UUIDMixin, AuditMixin
import os
from dotenv import load_dotenv

load_dotenv()
SCHEMA = os.getenv("DB_SCHEMA", "public")


class WetmillVisit(Base, SoftDeleteMixin, TimestampMixin, UUIDMixin, AuditMixin):
    __tablename__ = "wetmill_visits"
    __table_args__ = (
        Index("idx_wetmill_visits_wetmill_id", "wetmill_id"),
        Index("idx_wetmill_visits_user_id", "user_id"),
        Index("idx_wetmill_visits_submission_id", "submission_id"),
        Index("idx_wetmill_visits_created_by_id", "created_by_id"),
        Index("idx_wetmill_visits_last_updated_by_id", "last_updated_by_id"),
        {"schema": SCHEMA},
    )

    # Fields
    wetmill_id = Column(UUID(as_uuid=True), ForeignKey(f"{SCHEMA}.wetmills.id"), nullable=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey(f"{SCHEMA}.users.id"), nullable=True)
    form_name = Column(String, nullable=False)
    visit_date = Column(Date, nullable=False)
    entrance_photograph = Column(String, nullable=True)
    geo_location = Column(Geometry("POINT", srid=4326, spatial_index=False), nullable=True)
    submission_id = Column(String, nullable=False)

    # Relationship to wetmill and surveys
    wetmill = relationship("Wetmill", back_populates="visits")
    surveys = relationship(
        "WVSurveyResponse", back_populates="form_visit", cascade="all, delete-orphan"
    )
    submitter = relationship("User", back_populates="wetmill_visits", foreign_keys=[user_id])
