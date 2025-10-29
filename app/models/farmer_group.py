from sqlalchemy import Column, String, Integer, Boolean, ForeignKey, Index, Enum, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from .base import Base
from .mixins import AuditMixin, SoftDeleteMixin, TimestampMixin, UUIDMixin, SFIDMixin
from dotenv import load_dotenv
import os

load_dotenv()

SCHEMA = os.getenv("DB_SCHEMA", "public")


class FarmerGroup(
    Base, AuditMixin, SFIDMixin, TimestampMixin, UUIDMixin, SoftDeleteMixin
):
    __tablename__ = "farmer_groups"

    # Indexes and Constraints
    __table_args__ = (
        Index("idx_farmer_groups_project_id", "project_id"),
        Index("idx_farmer_groups_responsible_staff_id", "responsible_staff_id"),
        Index("idx_farmer_groups_tns_id", "tns_id"),
        Index("idx_farmer_groups_commcare_case_id", "commcare_case_id"),
        Index("idx_farmer_groups_sf_id", "sf_id"),
        Index("idx_farmer_groups_created_by_id", "created_by_id"),
        Index("idx_farmer_groups_last_updated_by_id", "last_updated_by_id"),
        {"schema": SCHEMA},
    )

    # Columns
    project_id = Column(
        UUID(as_uuid=True), ForeignKey(f"{SCHEMA}.projects.id"), nullable=False
    )
    responsible_staff_id = Column(
        UUID(as_uuid=True), ForeignKey(f"{SCHEMA}.users.id"), nullable=False
    )
    tns_id = Column(String, unique=True, nullable=False)
    commcare_case_id = Column(String, unique=True, nullable=False)
    ffg_name = Column(String, nullable=False)
    send_to_commcare = Column(
        Boolean, nullable=False, default=False, server_default=text("false")
    )
    send_to_commcare_status = Column(
        Enum(
            "Pending",
            "Processing",
            "Complete",
            name="farmer_group_send_to_commcare_status_enum",
            schema=SCHEMA
        ),
        nullable=False,
        default="Pending",
        server_default="Pending",
    )
    status = Column(
        Enum("Active", "Inactive", name="farmer_group_status_enum", schema=SCHEMA),
        nullable=False,
        default="Active",
        server_default="Active",
    )
    location_id = Column(
        UUID(as_uuid=True), ForeignKey(f"{SCHEMA}.locations.id"), nullable=False
    )
    fv_aa_sampling_round = Column(Integer, nullable=True)

    # Relationships
    project = relationship("Project", back_populates="farmer_groups")
    responsible_staff = relationship(
        "User", back_populates="farmer_groups", foreign_keys=[responsible_staff_id]
    )
    location = relationship("Location", back_populates="farmer_groups")
    farmers = relationship("Farmer", back_populates="farmer_group")
    households = relationship("Household", back_populates="farmer_group")
    training_sessions = relationship("TrainingSession", back_populates="farmer_group")
    observations = relationship("Observation", back_populates="farmer_group")
