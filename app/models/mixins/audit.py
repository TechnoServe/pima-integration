from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_mixin, declared_attr, relationship
import os

from dotenv import load_dotenv

load_dotenv()

SCHEMA = os.getenv("DB_SCHEMA", "public")


@declarative_mixin
class AuditMixin:

    @declared_attr
    def created_by_id(cls):  # pylint: disable=no-self-argument
        return Column(
            UUID(as_uuid=True), ForeignKey(f"{SCHEMA}.users.id"), nullable=False
        )

    @declared_attr
    def last_updated_by_id(cls):  # pylint: disable=no-self-argument
        return Column(
            UUID(as_uuid=True), ForeignKey(f"{SCHEMA}.users.id"), nullable=False
        )

    @declared_attr
    def creator(cls):  # pylint: disable=no-self-argument
        return relationship("User", foreign_keys=[cls.created_by_id])

    @declared_attr
    def last_updater(cls):  # pylint: disable=no-self-argument
        return relationship("User", foreign_keys=[cls.last_updated_by_id])
