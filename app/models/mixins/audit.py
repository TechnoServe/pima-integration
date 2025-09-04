from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_mixin, declared_attr, relationship
import os

SCHEMA = os.getenv("DB_SCHEMA", "public")

@declarative_mixin
class AuditMixin:

    @declared_attr
    def created_by_id(cls):
        return Column(UUID(as_uuid=True), ForeignKey(f"{SCHEMA}.users.id"), nullable=True)

    @declared_attr
    def last_updated_by_id(cls):
        return Column(UUID(as_uuid=True), ForeignKey(f"{SCHEMA}.users.id"), nullable=True)

    @declared_attr
    def creator(cls):
        return relationship("User", foreign_keys=[cls.created_by_id])

    @declared_attr
    def last_updater(cls):
        return relationship("User", foreign_keys=[cls.last_updated_by_id])