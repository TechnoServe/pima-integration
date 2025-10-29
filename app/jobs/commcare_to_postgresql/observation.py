from sqlalchemy.orm import Session
from services import (
    ForeignKeyResolver,
    ObservationService,
    ObservationResultService,
    ImageService,
    CheckService
)
from transformations import (
    ObservationTransformer,
    ObservationResultTransformer,
    CheckTransformer,
    ImageTransformer,
)
from models import Observation, ObservationResult, Check
from core import logger, DPO_MAPPINGS, DPO_RESULT_CRITERIA


class ObservationOrchestrator:
    """Orchestrates the entire ingestion process"""

    def __init__(self, db: Session):
        self.db = db
        self.resolver = ForeignKeyResolver(db)
        self.observation_transformer = ObservationTransformer(self.resolver)
        self.observation_service = ObservationService(db)
        self.observation_result_transformer = ObservationResultTransformer(
            self.resolver
        )
        self.observation_result_service = ObservationResultService(db)
        self.image_transformer = ImageTransformer()
        self.image_service = ImageService(self.db)
        self.check_transformer = CheckTransformer(self.resolver)
        self.check_service = CheckService(db)
        self.observation_result_criteria = DPO_RESULT_CRITERIA

    def process_data(self, raw_payload: dict, created_by_id: str):
        """Entry point for observation processing"""
        # Process observation data
        return self.process_observation(raw_payload, created_by_id)

    def process_observation(self, raw_payload: dict, created_by_id: str) -> Observation:
        """Complete workflow for processing observation payload"""

        try:
            # Step 1: Parse raw JSON into Pydantic schema
            payload = raw_payload

            # Step 2: Transform payload (includes foreign key resolution)
            transformed_data = self.observation_transformer.transform(payload)

            # Step 3: Upsert to database
            result = self.observation_service.upsert(transformed_data, created_by_id)

            logger.info({f"Upserted observation with record ID: '{result.id}'"})

            # Step 4: Upsert associated images if any
            image_url = payload.get("attachments", {}).get(
                payload.get("form", {}).get("Demo_Plot_Photo", ""), {}
            ).get("url", "") or payload.get("attachments", {}).get(
                payload.get("form", {}).get("Photo", ""), {}
            ).get(
                "url", ""
            )

            image_description = (
                "Demo Plot Photo"
                if payload.get("form", {}).get("Demo_Plot_Photo")
                else "Attendees Photo"
            )

            if image_url:
                self.process_image(
                    image_url=image_url,
                    payload=payload,
                    image_reference_obj=result,
                    image_description=image_description,
                    created_by_id=created_by_id,
                )

            # Step 5: Upsert observation results - Observer Feedback
            observer_feedback = payload.get("form", {}).get("Ratings_and_Comments")

            if observer_feedback:
                for question, answer in observer_feedback.items():
                    cleaned_payload = {
                        "submission_id": f"{payload.get('id')}-{question}",
                        "criterion": "Observer Feedback",
                        "question_key": question,
                        "result_text": answer,
                        "result_numeric": None,
                        "result_boolean": None,
                        "result_url": None,
                        "observation_id": result.id,
                    }
                    self.process_observation_result(
                        raw_payload=raw_payload,
                        cleaned_payload=cleaned_payload,
                        created_by_id=created_by_id,
                    )

            # Step 6: Upsert observation results - Participant Feedback
            participants = ["One", "Two", "Three"]

            participant_feedback = {}

            for participant in participants:
                key_prefix = f"Participant_{participant}_Feedback"
                feedback_data = payload.get("form", {}).get(key_prefix, {})

                if isinstance(feedback_data, dict):
                    for sub_key, value in feedback_data.items():
                        # Merge into flat dictionary with prefixed key
                        if sub_key in [
                            "participant_count",
                            "Attendend_Previous_Training_Module",
                            "participant_selected",
                            "participant_name",
                        ]:
                            continue
                        participant_feedback[f"{key_prefix}_{sub_key}"] = value

            if participant_feedback:
                for question, answer in participant_feedback.items():
                    cleaned_payload = {
                        "submission_id": f"{payload.get('id')}-{question}",
                        "criterion": "Participant Feedback",
                        "question_key": question,
                        "result_text": answer,
                        "result_numeric": None,
                        "result_boolean": None,
                        "result_url": None,
                    }
                    self.process_observation_result(
                        raw_payload=raw_payload,
                        cleaned_payload=cleaned_payload,
                        created_by_id=created_by_id,
                    )
            # Case for Kenya
            if (
                payload.get("app_id", "") == "30cee26f064e403388e334ae7b0c403b"
                and payload.get("metadata", {}).get("app_build_version", 0) >= 217
            ) or (
                payload.get("app_id", "") == "812728b8b35644dabb51561420938ee0"
                and payload.get("metadata", {}).get("app_build_version", 0) > 34
            ):
                for participant in participants:
                    cleaned_payload = payload.get("form", {}).get(
                        f"Participant_{participant}_Feedback", {}
                    )
                    self.process_check(
                        raw_payload=raw_payload,
                        cleaned_payload=cleaned_payload,
                        check_type="Training Observation",
                        created_by_id=created_by_id
                    )

            # Step 7: Upsert Demo Plot BP results
            for section, criterion in self.observation_result_criteria.items():
                section_payload = (
                    payload.get("form", {})
                    .get("best_practice_questions", {})
                    .get(section)
                )
                if not section_payload:
                    continue
                photo = None
                for question, answer in section_payload.items():
                    if question.endswith("_Photo") or question.endswith("_photo"):
                        photo = answer

                for question, answer in section_payload.items():
                    if question.endswith("_Photo") or question.endswith("_photo"):
                        continue
                    if question in ["covercrop_present", "pruning_methods"]:
                        for split_answer in answer.split(" "):
                            cleaned_payload = {
                                "submission_id": f"{payload.get('id')}-{question}-{split_answer}",
                                "criterion": criterion,
                                "question_key": question,
                                "result_text": DPO_MAPPINGS.get(question, {}).get(
                                    split_answer, None
                                ),
                                "result_numeric": None,
                                "result_boolean": None,
                                "result_url": None,
                                "photo": photo,
                            }
                            self.process_observation_result(
                                raw_payload=payload,
                                cleaned_payload=cleaned_payload,
                                created_by_id=created_by_id,
                            )
                        continue
                    cleaned_payload = {
                        "submission_id": f"{payload.get('id')}-{question}",
                        "criterion": criterion,
                        "question_key": question,
                        "result_text": DPO_MAPPINGS.get(question, {}).get(answer, None),
                        "result_numeric": (
                            float(answer)
                            if DPO_MAPPINGS.get(question, {}).get(answer, None) is None
                            else None
                        ),
                        "result_boolean": None,
                        "result_url": None,
                        "photo": photo,
                    }
                    self.process_observation_result(
                        raw_payload=payload,
                        cleaned_payload=cleaned_payload,
                        created_by_id=created_by_id,
                    )

            return result

        except ValueError as e:
            self.db.rollback()
            logger.error(
                {"message": f"Value error in observation processing: {str(e)}"}
            )
            raise

        except Exception as e:
            logger.error({f"Error processing observation: {str(e)}"})
            self.db.rollback()
            raise

    def process_observation_result(
        self, raw_payload: dict, cleaned_payload: dict, created_by_id: str
    ) -> ObservationResult:
        """Complete workflow for processing observation result payload"""

        try:
            # Step 1: Parse raw JSON into Pydantic schema
            payload = cleaned_payload

            # Step 2: Transform payload (includes foreign key resolution)
            transformed_data = self.observation_result_transformer.transform(
                raw_payload=raw_payload, cleaned_payload=cleaned_payload
            )

            # Step 3: Upsert to database
            result = self.observation_result_service.upsert(
                transformed_data, created_by_id
            )

            logger.info({f"Upserted observation result with record ID: '{result.id}'"})

            # Step 4: Upsert associated images if any
            image_url = (
                raw_payload.get("attachments", {})
                .get(payload.get("photo"), {})
                .get("url", "")
            )

            if image_url:
                self.process_image(
                    image_url=image_url,
                    payload=raw_payload,
                    image_reference_obj=result,
                    image_description=cleaned_payload.get("criterion"),
                    created_by_id=created_by_id,
                )

            return result

        except ValueError as e:
            self.db.rollback()
            logger.error(
                {"message": f"Value error in observation result processing: {str(e)}"}
            )
            raise

        except Exception as e:
            logger.error({f"Error processing observation result: {str(e)}"})
            self.db.rollback()
            raise


    def process_check(
        self,
        raw_payload: dict,
        cleaned_payload: dict,
        check_type: str,
        created_by_id: str,
    ) -> Check:
        """Function to process the TO checks"""
        try:

            # Step 1: Transform payload (includes foreign key resolution)
            transformed_data = self.check_transformer.transform(
                raw_payload=raw_payload,
                cleaned_payload=cleaned_payload,
                check_type=check_type,
            )

            # Step 2: Upsert to database
            result = self.check_service.upsert(transformed_data, created_by_id)

            logger.info({f"Upserted TO check with record ID: '{result.id}'"})

            return result

        except ValueError as e:
            self.db.rollback()
            logger.error({"message": f"Value error in TO  processing: {str(e)}"})
            raise

        except Exception as e:
            logger.error({f"Error processing TO check: {str(e)}"})
            self.db.rollback()
            raise
        
        
    def process_image(
        self,
        image_url: str,
        payload: dict,
        image_reference_obj: object,
        image_description: str,
        created_by_id: str,
    ):
        """Placeholder for image processing logic"""

        try:
            if image_url:
                image_data = self.image_transformer.transform(
                    payload=payload,
                    image_url=image_url,
                    image_reference_obj=image_reference_obj,
                    image_description=image_description,
                )

                image_result = self.image_service.upsert(image_data, created_by_id)

                logger.info(
                    {
                        f"Upserted image with record ID: '{image_result.id}' for observation ID: '{image_reference_obj.id}'"
                    }
                )

                return image_result
        except ValueError as e:
            self.db.rollback()
            logger.error({"message": f"Value error in image processing: {str(e)}"})
            raise
        except Exception as e:
            self.db.rollback()
            logger.error({"message": f"Unexpected error in image processing: {str(e)}"})
            raise
