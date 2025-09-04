from sqlalchemy import Column, String, Integer, Date, Boolean, Numeric, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
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

class Program(Base, AuditMixin, TimestampMixin, SoftDeleteMixin, SFIDMixin, UUIDMixin):
    __tablename__ = "programs"
    __table_args__ = {'schema': SCHEMA}
    
    # Columns
    program_name = Column(String, nullable=False)
    program_code = Column(String, nullable=False, unique=True)
    
    # Relationships
    projects = relationship("Project", back_populates="program")