from typing import Optional
from decimal import Decimal
from datetime import date
from uuid import UUID
from pydantic import BaseModel


class FarmCreate(BaseModel):
    """Pydantic model for validating the JSON for FIS Farm"""

    submission_id: str
    farm_visit_id: UUID
    household_id: UUID
    farm_name: str
    location_gps_latitude: Decimal
    location_gps_longitude: Decimal
    location_gps_altitude: Decimal
    farm_size_coffee_trees: int
    farm_size_land_measurements: Decimal
    main_coffee_field: bool
    planting_month_and_year: date
    planted_out_of_season: bool
    tns_id: str
    planted_out_of_season_comments: Optional[str]
    planted_on_visit_date: bool
