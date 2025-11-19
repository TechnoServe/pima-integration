from typing import Dict, Any
from schemas import FVBestPracticeAnswerCreate
from models import FVBestPractice
from services import ForeignKeyResolver
from core import (
    logger,
    FV_BP_MAPPINGS,
    FV_BP_VISIT_TYPE_FILTER,
    FV_STUMPING_PROGRAM_FILTER,
    FV_QUESTIONS_MAPPINGS,
    YN,
    YN_QUESTIONS
)
from pydantic import ValidationError


class FVBestPracticeAnswerTransformer:
    """Transforms CommCare payload to database-ready schema"""

    def __init__(self, resolver: ForeignKeyResolver):
        self.resolver = resolver

    def transform(
        self,
        payload: Dict,
        bp: str,
        bp_question: str,
        bp_answer: str,
        multiselect: bool,
        other: str
    ) -> FVBestPracticeAnswerCreate:
        """Transform CommCare payload to FVBestPracticeAnswerCreate schema"""
        try:

            session_data = self._map_fv_best_practice_answer_data(
                payload, bp_question, bp_answer, multiselect, other
            )

            # print(f"Final Session Data: {dict(session_data)}")

            fv_best_practice_id = self.resolver.resolve_db_id(
                f"FVBP-{payload.get("id")}-{bp}",
                FVBestPractice.submission_id,
                "FV Best Practice",
                FVBestPractice,
            ).id

            return FVBestPracticeAnswerCreate(
                fv_best_practice_id=fv_best_practice_id, **session_data
            )

        except ValidationError as e:
            logger.error(
                {"message": "Schema validation failed", "errors": str(e.errors())}
            )
            raise ValueError(f"Schema validation failed: {str(e.errors())}") from e

    def _map_fv_best_practice_answer_data(
        self, payload: Dict, bp_question: str, bp_answer: str, multiselect: bool, other: str
    ) -> Dict[str, Any]:
        """Map fv_best_practice_answer data"""
        visit_type = payload.get("form", {}).get("survey_type", "")
        app_id = payload.get("app_id", "")
        answer: str | None = None
        answer_numeric: float | None = None
        answer_boolean: bool | None = None

        if bp_question in FV_BP_MAPPINGS and bp_question in FV_BP_VISIT_TYPE_FILTER:
            answer = (
                FV_BP_MAPPINGS.get(bp_question, {})
                .get(visit_type, {})
                .get(bp_answer, "")
            )
            answer = f"Other: {other}" if answer == "Other" else answer

        # Special stumping year case
        elif bp_question == "year_stumping":
            answer = (
                FV_BP_MAPPINGS.get(bp_question, {})
                .get(FV_STUMPING_PROGRAM_FILTER.get(app_id, ""), "")
                .get(bp_answer, "")
            )
        elif (
            bp_question in FV_BP_MAPPINGS and bp_question not in FV_BP_VISIT_TYPE_FILTER
        ):
            answer = FV_BP_MAPPINGS.get(bp_question, {}).get(bp_answer, "")
            answer = f"Other: {other}" if answer == "Other" else answer
            if answer in ["Yes", "No"]:
                answer_boolean = answer == "Yes"
                answer = None

        elif bp_question in FV_QUESTIONS_MAPPINGS:
            answer = FV_QUESTIONS_MAPPINGS.get(bp_question, {}).get(bp_answer, "")
            answer = f"Other: {other}" if answer == "Other" else answer
        
        elif bp_question.endswith(tuple(YN_QUESTIONS)):
            answer_boolean = YN.get(bp_answer)

        elif not any(word in bp_question.lower() for word in ["photo", "image"]):
            try:
                answer_numeric = int(bp_answer)
            except (ValueError, TypeError):
                try:
                    answer_numeric = float(bp_answer)
                except (ValueError, TypeError):
                    answer = bp_answer

        return {
            "submission_id": (
                f"FVBPA-{payload.get('id')}-{bp_question}-{bp_answer}"
                if multiselect == True
                else f"FVBPA-{payload.get('id')}-{bp_question}"
            ),
            "question_key": bp_question,
            "answer_text": answer,
            "answer_numeric": answer_numeric,
            "answer_boolean": answer_boolean,
            "answer_url": None,
        }
