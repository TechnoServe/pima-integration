from sqlalchemy import (
    Column,
    String,
    Integer,
    Boolean,
    ForeignKey,
    Enum,
    CheckConstraint,
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


class Farmer(Base, AuditMixin, SFIDMixin, SoftDeleteMixin, TimestampMixin, UUIDMixin):
    __tablename__ = "farmers"

    # Indexes and Constraints
    __table_args__ = (
        Index("idx_farmers_household_id", "household_id"),
        Index("idx_farmers_farmer_group_id", "farmer_group_id"),
        Index("idx_farmers_tns_id", "tns_id"),
        Index("idx_farmers_commcare_case_id", "commcare_case_id"),
        Index("idx_farmers_sf_id", "sf_id"),
        Index("idx_farmers_created_by_id", "created_by_id"),
        Index("idx_farmers_last_updated_by_id", "last_updated_by_id"),
        CheckConstraint(
            "age >= 0 AND age <= 100", name="check_age_non_negative_and_reasonable"
        ),
        {"schema": SCHEMA},
    )

    # Columns
    household_id = Column(
        UUID(as_uuid=True), ForeignKey(f"{SCHEMA}.households.id"), nullable=False
    )
    farmer_group_id = Column(
        UUID(as_uuid=True), ForeignKey(f"{SCHEMA}.farmer_groups.id"), nullable=False
    )
    tns_id = Column(String, unique=False, nullable=False)
    commcare_case_id = Column(String, unique=True, nullable=False)
    first_name = Column(String, nullable=False)
    middle_name = Column(String, nullable=True)
    last_name = Column(String, nullable=False)
    other_id = Column(String, nullable=True)
    gender = Column(Enum("Male", "Female", name="farmer_gender_enum", schema=SCHEMA), nullable=False)
    age = Column(Integer, nullable=False)
    phone_number = Column(String, nullable=True)
    is_primary_household_member = Column(
        Boolean, default=False, server_default=text("false")
    )
    status = Column(
        Enum("Active", "Inactive", name="farmer_status_enum", schema=SCHEMA),
        nullable=False,
        default="Active",
        server_default="Active",
    )
    send_to_commcare = Column(
        Boolean, nullable=False, default=False, server_default=text("false")
    )
    send_to_commcare_status = Column(
        Enum(
            "Pending",
            "Processing",
            "Complete",
            name="farmer_send_to_commcare_status_enum",
            schema=SCHEMA
        ),
        nullable=False,
        default="Pending",
        server_default="Pending",
    )
    status_notes = Column(String, nullable=True)

    # Relationships
    farmer_group = relationship("FarmerGroup", back_populates="farmers")
    household = relationship("Household", back_populates="farmers")
    attendances = relationship("Attendance", back_populates="farmer")
    farm_visits_primary_farmer = relationship(
        "FarmVisit",
        back_populates="primary_farmer",
        foreign_keys="FarmVisit.visited_primary_farmer_id",
    )
    farm_visits_secondary_farmer = relationship(
        "FarmVisit",
        back_populates="secondary_farmer",
        foreign_keys="FarmVisit.visited_secondary_farmer_id",
    )
    checks = relationship("Check", back_populates="farmer")
