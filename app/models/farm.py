from sqlalchemy import (
    Column,
    String,
    Integer,
    Date,
    Boolean,
    Numeric,
    ForeignKey,
    Index,
    CheckConstraint,
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


class Farm(Base, AuditMixin, SFIDMixin, SoftDeleteMixin, TimestampMixin, UUIDMixin):
    __tablename__ = "farms"

    # Indexes and Constraints
    __table_args__ = (
        Index("idx_farms_farm_visit_id", "farm_visit_id"),
        Index("idx_farms_household_id", "household_id"),
        Index("idx_farms_submission_id", "submission_id"),
        Index("idx_farms_sf_id", "sf_id"),
        Index("idx_farms_tns_id", "tns_id"),
        Index("idx_farms_created_by_id", "created_by_id"),
        Index("idx_farms_last_updated_by_id", "last_updated_by_id"),
        CheckConstraint(
            "farm_size_land_measurements >= 0",
            name="check_farm_size_land_measurements_non_negative",
        ),
        CheckConstraint(
            "farm_size_coffee_trees >= 0",
            name="check_farm_size_coffee_trees_non_negative",
        ),
        CheckConstraint(
            "planting_month_and_year <= CURRENT_DATE",
            name="check_planting_month_and_year_not_in_future",
        ),
        {"schema": SCHEMA},
    )

    # Columns
    submission_id = Column(String, nullable=False, unique=True)
    farm_visit_id = Column(
        UUID(as_uuid=True), ForeignKey(f"{SCHEMA}.farm_visits.id"), nullable=False
    )
    household_id = Column(
        UUID(as_uuid=True), ForeignKey(f"{SCHEMA}.households.id"), nullable=False
    )
    farm_name = Column(String, nullable=False)
    location_gps_latitude = Column(Numeric(10, 6), nullable=False)
    location_gps_longitude = Column(Numeric(10, 6), nullable=False)
    location_gps_altitude = Column(Numeric(10, 2), nullable=False)
    farm_size_coffee_trees = Column(Integer, nullable=False)
    farm_size_land_measurements = Column(Numeric(10, 6), nullable=False)
    main_coffee_field = Column(
        Boolean, default=False, server_default=text("false"), nullable=False
    )
    planting_month_and_year = Column(Date, nullable=False)
    planted_out_of_season = Column(
        Boolean, default=False, server_default=text("false"), nullable=False
    )
    tns_id = Column(String, nullable=False, unique=True)
    planted_out_of_season_comments = Column(String, nullable=True)
    planted_on_visit_date = Column(
        Boolean, nullable=False, default=False, server_default=text("false")
    )

    # Relationships
    farm_visit = relationship("FarmVisit", back_populates="farms")
    household = relationship("Household", back_populates="farms")
    coffee_varieties = relationship(
        "CoffeeVariety", back_populates="farm", cascade="all, delete-orphan"
    )
