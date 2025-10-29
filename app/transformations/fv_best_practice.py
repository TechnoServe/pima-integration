"""FV Best Practice JSON Transformer"""

from typing import Dict, Any
from schemas import FVBestPracticeCreate
from services import ForeignKeyResolver
from models import FarmVisit
from pydantic import ValidationError
from core import logger, FV_BP_TYPE


class FVBestPracticeTransformer:
    """Transforms CommCare payload to database-ready schema"""

    def __init__(self, resolver: ForeignKeyResolver):
        self.resolver = resolver

    def transform(self, payload: Dict, bp: str) -> FVBestPracticeCreate:
        """Transform CommCare payload to FVBestPracticeCreate schema"""

        try:
            session_data = self._map_fv_best_practice(payload, bp)

            # Resolve foreign keys first
            farm_visit_id = self.resolver.resolve_db_id(
                f"FV-{payload.get("id")}",
                FarmVisit.submission_id,
                "Farm Visit",
                FarmVisit,
            ).id

            return FVBestPracticeCreate(
                farm_visit_id=farm_visit_id,
                **session_data,
            )
        except ValidationError as e:
            logger.error(
                {"message": "Schema validation failed", "errors": str(e.errors())}
            )
            raise ValueError(f"Schema validation failed: {str(e.errors())}") from e

    def _map_fv_best_practice(self, payload: Dict, bp: str) -> Dict[str, Any]:
        """Map data for FV Best Practice"""

        return {
            "submission_id": f"FVBP-{payload.get("id")}-{bp}",
            "best_practice_type": FV_BP_TYPE.get(bp, ""),
            "is_bp_verified": False
        }
