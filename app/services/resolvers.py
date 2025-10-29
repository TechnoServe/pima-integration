from typing import Dict, Type, Any
from sqlalchemy.orm import Session
from core import logger


class ForeignKeyResolver:
    """Handles resolution of external IDs to internal database records"""

    def __init__(self, db: Session):
        self.db = db
        self.cache: Dict[str, Any] = {}  # Cache model instances

    def resolve_db_id(
        self, external_id: str, id_column: object, field: str, model: Type
    ) -> Any:
        """Resolve external ID to an existing DB model instance"""
        if not external_id:
            raise ValueError(f"Missing external ID for '{field}'")

        cache_key = f"{field}:{external_id}"
        if cache_key in self.cache:
            logger.info(
                {
                    "message": f"Cached record for '{field}' with external ID '{external_id}'"
                }
            )
            return self.cache[cache_key]

        try:
            existing_record = (
                self.db.query(model)
                .filter(id_column == external_id, model.is_deleted == False)
                .first()
            )

            if existing_record:
                self.cache[cache_key] = existing_record
                logger.info(
                    {
                        "message": f"Resolved {field}: external_id={external_id}, internal_id={existing_record.id}"
                    }
                )
                return existing_record

            raise ValueError(
                f"No record found for '{field}' with external ID '{external_id}'"
            )

        except Exception as e:
            logger.error(
                {
                    "message": f"Error while resolving '{field}' with external ID '{external_id}'",
                    "error": str(e),
                }
            )
            raise
