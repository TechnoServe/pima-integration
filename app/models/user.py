from sqlalchemy import Column, String, ForeignKey, Enum, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from .base import Base
from .mixins import SoftDeleteMixin, TimestampMixin, UUIDMixin, SFIDMixin
import os
from dotenv import load_dotenv

load_dotenv()
SCHEMA = os.getenv("DB_SCHEMA", "public")


class User(Base, SFIDMixin, SoftDeleteMixin, TimestampMixin, UUIDMixin):
    __tablename__ = "users"
    __table_args__ = (
        Index("idx_users_tns_id", "tns_id"),
        Index("idx_users_commcare_mobile_worker_id", "commcare_mobile_worker_id"),
        Index("idx_users_manager_id", "manager_id"),
        Index("idx_users_sf_id", "sf_id"),
        Index("idx_users_created_by_id", "created_by_id"),
        Index("idx_users_last_updated_by_id", "last_updated_by_id"),
        {"schema": SCHEMA},
    )

    # Fields
    first_name = Column(String, nullable=False)
    middle_name = Column(String, nullable=True)
    last_name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=True)
    user_role = Column(String, nullable=True)
    username = Column(String, unique=True, nullable=True)
    password = Column(String, nullable=True)
    tns_id = Column(String, nullable=False, unique=True)
    phone_number = Column(String, nullable=True)
    job_title = Column(String, nullable=True)
    status = Column(
        Enum("Active", "Inactive", name="user_status_enum", schema=SCHEMA),
        default="Active",
        server_default="Active",
    )
    commcare_mobile_worker_id = Column(
        String,
        nullable=True,
    )
    manager_id = Column(
        UUID(as_uuid=True), ForeignKey(f"{SCHEMA}.users.id"), nullable=True
    )

    # Self-referential FKs
    created_by_id = Column(
        UUID(as_uuid=True), ForeignKey(f"{SCHEMA}.users.id"), nullable=True
    )
    last_updated_by_id = Column(
        UUID(as_uuid=True), ForeignKey(f"{SCHEMA}.users.id"), nullable=True
    )

    # Relationships
    created_by = relationship(
        "User", remote_side="User.id", foreign_keys=[created_by_id]
    )
    last_updated_by = relationship(
        "User", remote_side="User.id", foreign_keys=[last_updated_by_id]
    )
    manager = relationship(
        "User",
        remote_side="User.id",
        back_populates="subordinates",
        foreign_keys=[manager_id],
    )
    subordinates = relationship(
        "User",
        back_populates="manager",
        cascade="all, delete-orphan",
        foreign_keys=[manager_id],
    )

    # External Relationships
    project_staff_roles = relationship(
        "ProjectStaffRole",
        back_populates="staff",
        foreign_keys="ProjectStaffRole.staff_id",
    )
    farmer_groups = relationship(
        "FarmerGroup",
        back_populates="responsible_staff",
        foreign_keys="FarmerGroup.responsible_staff_id",
    )
    training_sessions = relationship(
        "TrainingSession",
        back_populates="trainer",
        foreign_keys="TrainingSession.trainer_id",
    )
    observer_observations = relationship(
        "Observation", back_populates="observer", foreign_keys="Observation.observer_id"
    )
    trainer_observations = relationship(
        "Observation", back_populates="trainer", foreign_keys="Observation.trainer_id"
    )
    farm_visits = relationship(
        "FarmVisit",
        back_populates="visiting_staff",
        foreign_keys="FarmVisit.visiting_staff_id",
    )
    checks = relationship(
        "Check", back_populates="checker", foreign_keys="Check.checker_id"
    )

    wetmills = relationship(
        "Wetmill", back_populates="submitter", foreign_keys="Wetmill.user_id"
    )

    wetmill_visits = relationship(
        "WetmillVisit", back_populates="submitter", foreign_keys="WetmillVisit.user_id"
    )
