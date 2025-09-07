from sqlalchemy import Column, String, Integer, Date, Boolean, Numeric, ForeignKey, DateTime, Index, CheckConstraint, Enum
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

class FarmerGroup(Base, AuditMixin, SFIDMixin, TimestampMixin, UUIDMixin, SoftDeleteMixin):
    __tablename__ = "farmer_groups"
    
    # Indexes and Constraints
    __table_args__ = (
        Index("idx_farmer_groups_project_id", "project_id"),
        Index("idx_farmer_groups_responsible_staff_id", "responsible_staff_id"),
        Index("idx_farmer_groups_tns_id", "tns_id"),
        Index("idx_farmer_groups_commcare_case_id", "commcare_case_id"),
        {'schema': SCHEMA}
    )

    # Columns
    project_id = Column(UUID(as_uuid=True), ForeignKey(f"{SCHEMA}.projects.id"), nullable=True)
    responsible_staff_id = Column(UUID(as_uuid=True), ForeignKey(f"{SCHEMA}.staff.id"), nullable=True)
    tns_id = Column(String, unique=True, index=True, nullable=True)
    commcare_case_id = Column(String, unique=True, index=True, nullable=True)
    ffg_name = Column(String, nullable=True)
    send_to_commcare = Column(Boolean, default=False)
    send_to_commcare_status = Column(Enum("Pending", "Processing", "Complete", name="send_to_commcare_status_enum"), nullable=False, default="Pending")
    status = Column(Enum("Active", "Inactive", name="status_enum"), nullable=False, default="Active")
    location_id = Column(UUID(as_uuid=True), ForeignKey(f"{SCHEMA}.locations.id"), nullable=False)
    fv_aa_sampling_round = Column(Integer, nullable=True)
    
    # Relationships
    project = relationship("Project", back_populates="farmer_groups")
    responsible_staff = relationship("Staff", back_populates="farmer_groups")
    location = relationship("Location", back_populates="farmer_groups")
    farmers = relationship("Farmer", back_populates="farmer_group")
    households = relationship("Household", back_populates="farmer_group")
    training_sessions = relationship("TrainingSession", back_populates="farmer_group")
    observations = relationship("Observation", back_populates="farmer_group")