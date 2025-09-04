from sqlalchemy import Column, String, Integer, Date, Boolean, Numeric, ForeignKey, DateTime, Index
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

class ObservationResult(Base, AuditMixin, SFIDMixin, SoftDeleteMixin, TimestampMixin, UUIDMixin):
    __tablename__ = "observation_results"
    __table_args__ = (
        Index("idx_observation_results_observation_id", "observation_id"),
        Index("idx_observation_results_submission_id", "submission_id"),
        {'schema': SCHEMA}
    )
    
    # Columns
    submission_id = Column(String, nullable=False)
    observation_id = Column(UUID(as_uuid=True), ForeignKey(f"{SCHEMA}.observations.id"), nullable=False)
    criterion = Column(String, nullable=True)
    question_key = Column(String, nullable=True)
    result_text = Column(String, nullable=True)
    result_numeric = Column(Numeric, nullable=True)
    result_boolean = Column(Boolean, nullable=True)
    result_url = Column(String, nullable=True)
    
    # Relationships
    observation = relationship("Observation", back_populates="observation_results")