from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, backref
from .base import Base
from .mixins.sf_id import SFIDMixin
from .mixins.soft_delete import SoftDeleteMixin
from .mixins.timestamp import TimestampMixin
from .mixins.uuid import UUIDMixin
import os
from dotenv import load_dotenv

load_dotenv()
SCHEMA = os.getenv("DB_SCHEMA", "public")


class User(Base, SFIDMixin, SoftDeleteMixin, TimestampMixin, UUIDMixin):
    __tablename__ = "users"
    __table_args__ = {'schema': SCHEMA}
    
    # Fields
    first_name = Column(String, nullable=True)
    middle_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    email = Column(String, unique=True, index=True, nullable=True)
    usergroup = Column(String, nullable=True)
    username = Column(String, unique=True, index=True, nullable=True)
    password = Column(String, nullable=True)

    # Self-referential FKs
    created_by_id = Column(UUID(as_uuid=True), ForeignKey(f"{SCHEMA}.users.id"), nullable=True)
    last_updated_by_id = Column(UUID(as_uuid=True), ForeignKey(f"{SCHEMA}.users.id"), nullable=True)

    # Relationships
    created_by = relationship("User", remote_side="User.id", foreign_keys=[created_by_id])
    last_updated_by = relationship("User", remote_side="User.id", foreign_keys=[last_updated_by_id])