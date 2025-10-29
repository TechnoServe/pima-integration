from sqlalchemy import Column, String, Integer, ForeignKey, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from .base import Base
from .mixins import AuditMixin, SoftDeleteMixin, TimestampMixin, UUIDMixin, SFIDMixin
from dotenv import load_dotenv
import os

load_dotenv()

SCHEMA = os.getenv("DB_SCHEMA", "public")


class CoffeeVariety(
    Base, AuditMixin, SFIDMixin, SoftDeleteMixin, TimestampMixin, UUIDMixin
):
    __tablename__ = "coffee_varieties"
    __table_args__ = (
        Index("idx_coffee_varieties_farm_id", "farm_id"),
        Index("idx_coffee_varieties_submission_id", "submission_id"),
        Index("idx_coffee_varieties_sf_id", "sf_id"),
        Index("idx_coffee_varieties_created_by_id", "created_by_id"),
        Index("idx_coffee_varieties_last_updated_by_id", "last_updated_by_id"),
        {"schema": SCHEMA},
    )

    variety_name = Column(String, nullable=False)
    number_of_trees = Column(Integer, nullable=False)
    submission_id = Column(String, nullable=False, unique=True)
    farm_id = Column(
        UUID(as_uuid=True), ForeignKey(f"{SCHEMA}.farms.id"), nullable=False
    )

    # Relationships
    farm = relationship("Farm", back_populates="coffee_varieties")
