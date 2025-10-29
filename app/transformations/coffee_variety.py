"""FIS Coffee Variety JSON Transformer"""

from typing import Dict, Any
from schemas import CoffeeVarietyCreate
from models import Farm
from services import ForeignKeyResolver
from pydantic import ValidationError
from core import logger


class CoffeeVarietyTransformer:
    """Transforms CommCare payload to database-ready schema"""

    def __init__(self, resolver: ForeignKeyResolver):
        self.resolver = resolver

    def transform(self, cleaned_payload: Dict) -> CoffeeVarietyCreate:
        """Transform CommCare payload to CoffeeVarietyCreate schema"""

        try:

            session_data = self._map_variety(cleaned_payload)

            # Resolve foreign keys first
            
            farm_id = self.resolver.resolve_db_id(
                cleaned_payload.get("farm_submission_id"),
                Farm.submission_id,
                "Farm",
                Farm,
            ).id
            
            return CoffeeVarietyCreate(
                farm_id=farm_id,
                **session_data,
            )
        except ValidationError as e:
            logger.error(
                {"message": "Schema validation failed", "errors": str(e.errors())}
            )
            raise ValueError(f"Schema validation failed: {str(e.errors())}") from e

    def _map_variety(self, cleaned_payload: Dict) -> Dict[str, Any]:
        """Map data for FIS Farm Data"""

        return {
            "variety_name": {
                "1": "Costa Rica 95",
                "2": "SL28 or 34",
                "3": "K7",
                "4": "Catimor 129",
                "5": "Catuai",
                "6": "Yellow Catuai",
                "7": "F6",
                "8": "Caturra",
                "9": cleaned_payload.get("other_variety", "")
            }.get(cleaned_payload.get("variety"), ""),
            "number_of_trees": cleaned_payload.get("number_of_trees"),
            "submission_id": f'CV-0{cleaned_payload.get("variety")}-{cleaned_payload.get("farm_submission_id")}'
        }