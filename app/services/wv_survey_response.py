from models import WVSurveyResponse
from schemas import WVSurveyResponseCreate
from core import logger
from sqlalchemy.orm import Session

class WVSurveyResponseService:
    """Handles database operations for wetmill visit survey responses"""

    def __init__(self, db: Session):
        self.db = db

    def upsert(self, data: WVSurveyResponseCreate, created_by_id: str) -> WVSurveyResponse:
        """Create and Update wetmill visit survey response data"""

        # Look up existing wetmill visit
        existing = (
            self.db.query(WVSurveyResponse)
            .filter(
                WVSurveyResponse.submission_id == data.submission_id,
                WVSurveyResponse.is_deleted == False,
            )
            .first()
        )

        if existing:
            logger.info(
                {
                    "message": f"Updating existing wetmill visit survey response record: {data.submission_id}"
                }
            )
            return self._update_existing(existing, data, created_by_id)
        else:
            logger.info(
                {"message": f"Creating new wetmill visit survey response record: {data.submission_id}"}
            )
            return self._create_new(data, created_by_id)

    def _update_existing(
        self, existing: WVSurveyResponse, data: WVSurveyResponseCreate, updated_by_id: str
    ) -> WVSurveyResponse:
        """Update existing wetmill visit survey response with smart merging"""

        # Smart update: don't overwrite existing data with None values
        for field, value in data.model_dump(exclude_unset=True).items():
            if field in ["submission_id", "user_id"]:
                # Always update core fields
                setattr(existing, field, value)
            elif value is not None:
                current_value = getattr(existing, field, None)
                if current_value is None or value != current_value:
                    setattr(existing, field, value)

        existing.last_updated_by_id = updated_by_id

        self.db.commit()
        self.db.refresh(existing)
        return existing

    def _create_new(self, data: WVSurveyResponseCreate, created_by_id: str) -> WVSurveyResponse:
        """Create new wetmill visit survey response"""

        survey_response = WVSurveyResponse(
            **data.model_dump(exclude_unset=True),
            created_by_id=created_by_id,
            last_updated_by_id=created_by_id,
        )
        
        print(f"DATA: {str(data)}")
        print(f"CREATED BY: {created_by_id}")

        try:
            self.db.add(survey_response)
            self.db.commit()
            self.db.refresh(survey_response)
        except Exception as e:
            logger.error({
                "message": "DB insert failed",
                "exception": repr(e),
            })
            raise
        return survey_response
