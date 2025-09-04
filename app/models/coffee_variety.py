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

class CoffeeVariety(Base, AuditMixin, SFIDMixin, SoftDeleteMixin, TimestampMixin, UUIDMixin):
    __tablename__ = "coffee_varieties"
    __table_args__ = (
        Index("idx_coffee_varieties_farm_id", "farm_id"),
        Index("idx_coffee_varieties_submission_id", "submission_id"),
        Index("idx_coffee_varieties_sf_id", "sf_id"),
        {'schema': SCHEMA}
    )

    variety_name = Column(String, nullable=False)
    number_of_trees = Column(Integer, nullable=False)
    submission_id = Column(String, nullable=False, unique=True)
    farm_id = Column(UUID(as_uuid=True), ForeignKey(f"{SCHEMA}.farms.id"), nullable=False)
    
    # Relationships
    farm = relationship("Farm", back_populates="coffee_varieties")