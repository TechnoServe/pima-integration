from sqlalchemy import Column, String, Integer, Date, Boolean, Numeric, ForeignKey, DateTime, Enum
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

class ProjectStaffRole(Base, AuditMixin, TimestampMixin, SFIDMixin, SoftDeleteMixin, UUIDMixin):
    __tablename__ = "project_staff_roles"
    __table_args__ = {'schema': SCHEMA}

    # Columns
    project_id = Column(UUID(as_uuid=True), ForeignKey(f"{SCHEMA}.projects.id"), nullable=False)
    staff_id = Column(UUID(as_uuid=True), ForeignKey(f"{SCHEMA}.staff.id"), nullable=False)
    commcare_location_id = Column(String, nullable=True)
    commcare_case_id = Column(String, nullable=True, unique=True)
    tns_id = Column(String, nullable=True, unique=True)
    role = Column(String, nullable=False)
    status = Column(Enum("Active", "Inactive", name="status_enum"), nullable=False)
    send_to_commcare = Column(Boolean, nullable=False, default=False)
    send_to_commcare_status = Column(Enum("Pending", "Processing", "Complete", name="send_to_commcare_status_enum"), nullable=False, default="Pending")
    
    # Relationships
    project = relationship("Project", back_populates="project_staff_roles")
    staff = relationship("Staff", back_populates="project_staff_roles")