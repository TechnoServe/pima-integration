from sqlalchemy import Column, String, Boolean, ForeignKey, Enum, text, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from .base import Base
from .mixins import AuditMixin, SoftDeleteMixin, TimestampMixin, UUIDMixin, SFIDMixin
from dotenv import load_dotenv
import os

load_dotenv()


SCHEMA = os.getenv("DB_SCHEMA", "public")


class ProjectStaffRole(
    Base, AuditMixin, TimestampMixin, SFIDMixin, SoftDeleteMixin, UUIDMixin
):
    __tablename__ = "project_staff_roles"
    __table_args__ = (
        Index("idx_project_staff_roles_project_id", "project_id"),
        Index("idx_project_staff_roles_staff_id", "staff_id"),
        Index("idx_project_staff_roles_commcare_location_id", "commcare_location_id"),
        Index("idx_project_staff_roles_commcare_case_id", "commcare_case_id"),
        Index("idx_project_staff_roles_tns_id", "tns_id"),
        Index("idx_project_staff_roles_created_by_id", "created_by_id"),
        Index("idx_project_staff_roles_last_updated_by_id", "last_updated_by_id"),
        {"schema": SCHEMA},
    )

    # Columns
    project_id = Column(
        UUID(as_uuid=True), ForeignKey(f"{SCHEMA}.projects.id"), nullable=False
    )
    staff_id = Column(
        UUID(as_uuid=True), ForeignKey(f"{SCHEMA}.users.id"), nullable=False
    )
    commcare_location_id = Column(String, nullable=True)
    commcare_case_id = Column(String, nullable=False, unique=True)
    tns_id = Column(String, nullable=False, unique=True)
    role = Column(String, nullable=False)
    status = Column(
        Enum("Active", "Inactive", name="project_staff_role_status_enum", schema=SCHEMA),
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
            name="project_staff_role_send_to_commcare_status_enum",
            schema=SCHEMA
        ),
        nullable=False,
        default="Pending",
        server_default="Pending",
    )

    # Relationships
    project = relationship("Project", back_populates="project_staff_roles")
    staff = relationship(
        "User", back_populates="project_staff_roles", foreign_keys=[staff_id]
    )
