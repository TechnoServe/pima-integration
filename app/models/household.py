from sqlalchemy import (
    Column,
    String,
    Integer,
    Boolean,
    Numeric,
    ForeignKey,
    Enum,
    Index,
    text,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from .base import Base
from .mixins import AuditMixin, SoftDeleteMixin, TimestampMixin, UUIDMixin, SFIDMixin
from dotenv import load_dotenv
import os

load_dotenv()

SCHEMA = os.getenv("DB_SCHEMA", "public")


class Household(
    Base, AuditMixin, SFIDMixin, SoftDeleteMixin, TimestampMixin, UUIDMixin
):
    __tablename__ = "households"

    # Indexes and Constraints
    __table_args__ = (
        Index("idx_households_farmer_group_id", "farmer_group_id"),
        Index("idx_households_tns_id", "tns_id"),
        Index("idx_households_commcare_case_id", "commcare_case_id"),
        Index("idx_households_sf_id", "sf_id"),
        Index("idx_households_created_by_id", "created_by_id"),
        Index("idx_households_last_updated_by_id", "last_updated_by_id"),
        {"schema": SCHEMA},
    )

    # Columns
    farmer_group_id = Column(
        UUID(as_uuid=True), ForeignKey(f"{SCHEMA}.farmer_groups.id"), nullable=False
    )
    household_name = Column(String, nullable=False)
    household_number = Column(Integer, nullable=False)
    tns_id = Column(String, nullable=False, unique=True)
    commcare_case_id = Column(String, nullable=True, unique=True)
    number_of_trees = Column(Integer, nullable=True, default=0, server_default="0")
    farm_size = Column(Numeric(10, 6), nullable=True, default=0, server_default="0")
    sampled_for_fv_aa = Column(
        Boolean, nullable=False, default=False, server_default=text("false")
    )
    farm_size_before = Column(Numeric(10, 6), nullable=True)
    farm_size_after = Column(Numeric(10, 6), nullable=True)
    farm_size_since = Column(Numeric(10, 6), nullable=True)
    status = Column(
        Enum("Active", "Inactive", name="household_status_enum", schema=SCHEMA),
        nullable=False,
        default="Active",
        server_default="Active",
    )
    visited_for_fv_aa = Column(
        Boolean, nullable=False, default=False, server_default=text("false")
    )
    fv_aa_sampling_round = Column(
        Integer, nullable=False, default=0, server_default="0"
    )

    # Relationships
    farmers = relationship("Farmer", back_populates="household")
    farmer_group = relationship("FarmerGroup", back_populates="households")
    farms = relationship("Farm", back_populates="household")
    farm_visits = relationship("FarmVisit", back_populates="visited_household")
