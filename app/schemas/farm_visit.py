from typing import Optional, Literal
from decimal import Decimal
from uuid import UUID
from datetime import date
from pydantic import BaseModel


class FarmVisitCreate(BaseModel):
    """PyDantic Schema for validating the Farm Visit JSON"""

    visited_household_id: UUID
    visited_primary_farmer_id: UUID
    visited_secondary_farmer_id: Optional[UUID] = None
    submission_id: str
    training_session_id: Optional[UUID]
    visiting_staff_id: UUID
    date_visited: date
    farm_visit_type: Literal[
        "Farm Visit Full - ET",
        "Farm Visit Full - KE",
        "Farm Visit Full - PR",
        "Farm Visit Full - ZM",
    ]
    visit_comments: Optional[str]
    latest_visit: bool
    location_gps_latitude: Decimal
    location_gps_longitude: Decimal
    location_gps_altitude: Decimal
