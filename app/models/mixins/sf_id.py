from sqlalchemy import Column, ForeignKey, Boolean, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_mixin, relationship

@declarative_mixin
class SFIDMixin:
    from_sf = Column(Boolean, nullable=False, default=False)
    sf_id = Column(String, nullable=True, unique=True)