from sqlalchemy import Column, String, ForeignKey, Integer, Index, Text, Date
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from .base import Base
from .mixins import SoftDeleteMixin, TimestampMixin, UUIDMixin, AuditMixin
from geoalchemy2 import Geometry
import os
from dotenv import load_dotenv

load_dotenv()
SCHEMA = os.getenv("DB_SCHEMA", "public")


class Wetmill(Base, SoftDeleteMixin, TimestampMixin, UUIDMixin, AuditMixin):
    __tablename__ = "wetmills"
    __table_args__ = (
        Index("idx_wetmills_user_id", "user_id"),
        Index("idx_wetmills_wet_mill_unique_id", "wet_mill_unique_id"),
        Index("idx_wetmills_commcare_case_id", "commcare_case_id"),
        Index("idx_wetmills_programme", "programme"),
        Index("idx_wetmills_country", "country"),
        Index("idx_wetmills_created_by_id", "created_by_id"),
        Index("idx_wetmills_last_updated_by_id", "last_updated_by_id"),
        {"schema": SCHEMA},
    )

    # Fields
    user_id = Column(
        UUID(as_uuid=True), ForeignKey(f"{SCHEMA}.users.id"), nullable=True
    )
    wet_mill_unique_id = Column(String, nullable=False)
    commcare_case_id = Column(String, unique=True)
    name = Column(String)
    mill_status = Column(String)
    exporting_status = Column(String)
    programme = Column(String)
    country = Column(String)
    manager_name = Column(String, nullable=True)
    manager_role = Column(String, nullable=True)
    comments = Column(Text, nullable=True)
    wetmill_counter = Column(Integer, nullable=True)
    ba_signature = Column(String, nullable=True)
    manager_signature = Column(String, nullable=True)
    tor_page_picture = Column(String, nullable=True)
    registration_date = Column(Date, nullable=True)
    office_entrance_picture = Column(String, nullable=True)
    office_gps = Column(Geometry("POINT", srid=4326, spatial_index=False), nullable=True)

    # Relationship to visits
    visits = relationship(
        "WetmillVisit", back_populates="wetmill", cascade="all, delete-orphan"
    )
    submitter = relationship("User", back_populates="wetmills", foreign_keys=[user_id])
