from sqlalchemy.orm import Session
from core import logger, ALLOWED_SURVEYS, SURVEY_TRANSFORMATIONS
from models import (
    WetmillVisit,
    WVSurveyResponse,
    WVSurveyQuestionResponse,
)
from transformations import (
    WetmillVisitTransformer,
    WVSurveyResponseTransformer,
    WVSurveyQuestionResponseTransformer,
)
from services import (
    ForeignKeyResolver,
    WetmillVisitService,
    WVSurveyResponseService,
    WVSurveyQuestionResponseService,
)


class WetmillVisitOrchestrator:
    def __init__(self, db: Session):
        self.db = db
        self.resolver = ForeignKeyResolver(self.db)
        self.wetmill_visit_transformer = WetmillVisitTransformer(self.db)
        self.wetmill_visit_service = WetmillVisitService(self.db)
        self.wv_survey_response_transformer = WVSurveyResponseTransformer(self.db)
        self.wv_survey_response_service = WVSurveyResponseService(self.db)
        self.wv_survey_question_response_transformer = (
            WVSurveyQuestionResponseTransformer(self.db)
        )
        self.wv_survey_question_response_service = WVSurveyQuestionResponseService(
            self.db
        )

    def process_data(self, raw_payload: dict, created_by_id: str):
        """Complete workflow for processing wetmill visit"""

        # 1. Process wetmill visit
        return self.process_wetmill_visit(raw_payload, created_by_id)

    def process_wetmill_visit(
        self, raw_payload: dict, created_by_id: str
    ) -> WetmillVisit:
        payload = raw_payload

        # 1. Process Wetmill Visit
        try:
            transformed_data = self.wetmill_visit_transformer.transform(payload=payload)

            result = self.wetmill_visit_service.upsert(
                data=transformed_data, created_by_id=created_by_id
            )

            logger.info({f"Upserted wetmill visit with record ID: '{result.id}'"})

            surveys = payload.get("form", {}).get("surveys", {})
            for survey_name, content in surveys.items():
                if survey_name not in ALLOWED_SURVEYS:
                    print("skipping survey: " + survey_name)
                    continue
                if not isinstance(content, dict):  # Skip non survey
                    continue
                self.process_survey_reponse(
                    payload=payload,
                    survey_name=survey_name,
                    content=content,
                    created_by_id=created_by_id,
                )

            return result
        except ValueError as e:
            self.db.rollback()
            logger.error(
                {"message": f"Value error in wetmill visit processing: {str(e)}"}
            )
            raise

        except Exception as e:
            logger.error({f"Error processing wetmill visit: {str(e)}"})
            self.db.rollback()
            raise

    def process_survey_reponse(
        self,
        payload: dict,
        survey_name: str,
        content: dict,
        created_by_id: str,
    ) -> WVSurveyResponse:

        try:
            # Apply transformation functions (ETL) for each survey
            transform_func = SURVEY_TRANSFORMATIONS.get(survey_name)
            form = payload.get("form", {})
            url_string = f'https://www.commcarehq.org/a/{payload.get("domain")}/api/form/attachment/{payload.get("form", {}).get("meta", {}).get("instanceID")}'
            content = transform_func(content, url_string, form)

            transformed_data = self.wv_survey_response_transformer.transform(
                payload=payload, survey_type=survey_name, content=content
            )

            result = self.wv_survey_response_service.upsert(
                transformed_data, created_by_id
            )
            
            logger.info({f"Upserted wv survey response with record ID: '{result.id}'"})

            # Insert question responses
            for section, sec_content in content.items():
                # handle multiple answers questions on top level
                if isinstance(sec_content, list):
                    for item in sec_content:
                        item_index = str(sec_content.index(item) + 1)

                        submission_id = f"SQR-{payload.get("id")}-{survey_name}-{section}-{item_index}"

                        self.process_survey_question_response(
                            payload=payload,
                            survey_type=survey_name,
                            section_name=section,
                            question_name=section,
                            answer=item,
                            submission_id=submission_id,
                            created_by_id=created_by_id,
                        )

                # Nested questions
                elif isinstance(sec_content, dict):
                    for q_name, ans in sec_content.items():
                        # handle multiple answers questions in nested
                        if isinstance(ans, list):
                            for item in ans:
                                item_index = str(ans.index(item) + 1)  # 1-based index
                                submission_id = f"SQR-{payload.get("id")}-{survey_name}-{section}-{q_name}-{item_index}"
                                self.process_survey_question_response(
                                    payload=payload,
                                    survey_type=survey_name,
                                    section_name=section,
                                    question_name=q_name,
                                    answer=item,
                                    submission_id=submission_id,
                                    created_by_id=created_by_id,
                                )
                        else:
                            # Skip label fields
                            if q_name.endswith("_label"):
                                continue
                            submission_id = f"SQR-{payload.get("id")}-{survey_name}-{section}-{q_name}"
                            self.process_survey_question_response(
                                payload=payload,
                                survey_type=survey_name,
                                section_name=section,
                                question_name=q_name,
                                answer=ans,
                                submission_id=submission_id,
                                created_by_id=created_by_id,
                            )
                # Single value questions or flags
                else:
                    # Skip top-level label or survey keys
                    if section.endswith("_label") or section.startswith("survey_"):
                        continue
                    submission_id = f"SQR-{payload.get("id")}-{survey_name}-{section}"
                    self.process_survey_question_response(
                        payload=payload,
                        survey_type=survey_name,
                        section_name=None,
                        question_name=section,
                        answer=sec_content,
                        submission_id=submission_id,
                        created_by_id=created_by_id,
                    )

            return result

        except ValueError as e:
            self.db.rollback()
            logger.error(
                {"message": f"Value error in wv survey response processing: {str(e)}"}
            )
            raise

        except Exception as e:
            logger.error({f"Error processing wv survey response: {str(e)}"})
            self.db.rollback()
            raise

    def process_survey_question_response(
        self,
        payload: dict,
        survey_type: str,
        section_name: str,
        question_name: str,
        answer,
        submission_id,
        created_by_id,
    ) -> WVSurveyQuestionResponse:
        """
        Create and add a WVSurveyQuestionResponse for a given answer.
        """
        try:
            transformed_data = self.wv_survey_question_response_transformer.transform(
                payload=payload,
                survey_type=survey_type,
                section_name=section_name,
                question_name=question_name,
                answer=answer,
                submission_id=submission_id,
            )

            result = self.wv_survey_question_response_service.upsert(
                transformed_data, created_by_id
            )
            logger.info(
                {f"Upserted wv survey question response with record ID: '{result.id}'"}
            )
            return result
        except ValueError as e:
            self.db.rollback()
            logger.error(
                {
                    "message": f"Value error in wv survey question response processing: {str(e)}"
                }
            )
            raise

        except Exception as e:
            logger.error({f"Error processing wv survey question response: {str(e)}"})
            self.db.rollback()
            raise
