from sqlalchemy import Column, Boolean, DateTime, func, text
from sqlalchemy.orm import declarative_mixin

@declarative_mixin
class SoftDeleteMixin:
    is_deleted = Column(Boolean, default=False, server_default=text("false"), nullable=False)
    deleted_at = Column(DateTime(timezone=True), nullable=True)

    def soft_delete(self, deleted_at=None):
        """Mark record as deleted instead of removing it"""
        self.is_deleted = True
        self.deleted_at = deleted_at or func.now()