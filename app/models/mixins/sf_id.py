from sqlalchemy import Column, Boolean, String, text
from sqlalchemy.orm import declarative_mixin


@declarative_mixin
class SFIDMixin:
    from_sf = Column(
        Boolean, nullable=False, default=False, server_default=text("false")
    )
    sf_id = Column(String, nullable=True, unique=True)
