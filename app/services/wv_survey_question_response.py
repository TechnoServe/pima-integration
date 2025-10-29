from models import WVSurveyQuestionResponse
from schemas import WVSurveyQuestionResponseCreate
from core import logger
from sqlalchemy.orm import Session

class WVSurveyQuestionResponseService:
    """Handles database operations for wetmill visit survey question responses"""

    def __init__(self, db: Session):
        self.db = db

    def upsert(self, data: WVSurveyQuestionResponseCreate, created_by_id: str) -> WVSurveyQuestionResponse:
        """Create and Update wetmill visit survey question response data"""

        # Look up existing wetmill visit
        existing = (
            self.db.query(WVSurveyQuestionResponse)
            .filter(
                WVSurveyQuestionResponse.submission_id == data.submission_id,
                WVSurveyQuestionResponse.is_deleted == False,
            )
            .first()
        )

        if existing:
            logger.info(
                {
                    "message": f"Updating existing wetmill visit survey question response record: {data.submission_id}"
                }
            )
            return self._update_existing(existing, data, created_by_id)
        else:
            logger.info(
                {"message": f"Creating new wetmill visit survey question response record: {data.submission_id}"}
            )
            return self._create_new(data, created_by_id)

    def _update_existing(
        self, existing: WVSurveyQuestionResponse, data: WVSurveyQuestionResponseCreate, updated_by_id: str
    ) -> WVSurveyQuestionResponse:
        """Update existing wetmill visit survey question response with smart merging"""

        # Smart update: don't overwrite existing data with None values
        for field, value in data.model_dump(exclude_unset=True).items():
            if field in ["submission_id"]:
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

    def _create_new(self, data: WVSurveyQuestionResponseCreate, created_by_id: str) -> WVSurveyQuestionResponse:
        """Create new wetmill visit survey question response"""

        survey_question_response = WVSurveyQuestionResponse(
            **data.model_dump(exclude_unset=True),
            created_by_id=created_by_id,
            last_updated_by_id=created_by_id,
        )

        try:
            self.db.add(survey_question_response)
            self.db.commit()
            self.db.refresh(survey_question_response)
        except Exception as e:
            logger.error({
                "message": "DB insert failed",
                "exception": repr(e),
                # "traceback": traceback.format_exc()
            })
            raise
        return survey_question_response
