from sqlalchemy.orm import Session
from services import (
    ForeignKeyResolver,
    FarmVisitService,
    FVBestPracticeService,
    FVBestPracticeAnswerService,
    ImageService,
    FarmService,
    CoffeeVarietyService,
    CheckService,
)
from transformations import (
    FarmVisitTransformer,
    FVBestPracticeTransformer,
    FVBestPracticeAnswerTransformer,
    ImageTransformer,
    CoffeeVarietyTransformer,
    FarmTransformer,
    CheckTransformer,
)
from models import (
    FarmVisit,
    FVBestPractice,
    FVBestPracticeAnswer,
    Image,
    Farm,
    CoffeeVariety,
    Check,
)
from core import logger, FV_BP_TYPE, FV_BP_MULTISELECT, FV_QUESTIONS_IGNORE_LIST
from jobs.commcare_to_postgresql.participant_registration_and_update import ParticipantRegistrationAndUpdateOrchestrator


class FarmVisitOrchestrator:
    """Orchestrates the entire ingestion process"""

    def __init__(self, db: Session):
        self.db = db
        self.resolver = ForeignKeyResolver(db)
        self.farm_visit_transformer = FarmVisitTransformer(self.resolver)
        self.farm_visit_service = FarmVisitService(db)
        self.fv_best_practice_transformer = FVBestPracticeTransformer(self.resolver)
        self.fv_best_practice_service = FVBestPracticeService(db)
        self.fv_best_practice_answer_transformer = FVBestPracticeAnswerTransformer(
            self.resolver
        )
        self.fv_best_practice_answer_service = FVBestPracticeAnswerService(db)
        self.image_transformer = ImageTransformer()
        self.image_service = ImageService(db)
        self.farm_transformer = FarmTransformer(self.resolver)
        self.farm_service = FarmService(db)
        self.variety_transformer = CoffeeVarietyTransformer(self.resolver)
        self.variety_service = CoffeeVarietyService(db)
        self.check_transformer = CheckTransformer(self.resolver)
        self.check_service = CheckService(db)
        self.best_practice_type = FV_BP_TYPE
        self.participant_registration = ParticipantRegistrationAndUpdateOrchestrator(db)

    def process_data(self, raw_payload: dict, created_by_id: str):
        """Entry point for farm visit processing"""

        # Process participant registration
        pr_registration_fv = (
            raw_payload.get("form", {}).get("survey_type", "") == "Farm Visit Full - PR"
            and raw_payload.get("form", {}).get("new_farmer", "") == "1"
        )
        if pr_registration_fv:
            self.participant_registration.process_data(raw_payload, created_by_id)
        else:
            logger.info({"message": "Skipping participant registration"})

        # Process farm visit data
        return self.process_farm_visit(raw_payload, created_by_id)

    def process_farm_visit(self, raw_payload: dict, created_by_id: str) -> FarmVisit:
        """Complete workflow for processing farm visit payload"""

        try:
            # Step 1: Parse raw JSON into Pydantic schema
            payload = raw_payload

            # Step 2: Transform payload (includes foreign key resolution)
            transformed_data = self.farm_visit_transformer.transform(payload)

            # Step 3: Upsert to database
            result = self.farm_visit_service.upsert(transformed_data, created_by_id)

            logger.info({f"Upserted farm visit with record ID: '{result.id}'"})

            # Step 4: Upsert associated images if any
            image_url = (
                payload.get("attachments", {})
                .get(payload.get("form", {}).get("farm_visit_photo", ""), {})
                .get("url", "")
            )

            if image_url:
                self.process_image(
                    image_url=image_url,
                    payload=payload,
                    image_reference_obj=result,
                    image_description="Farm Visit Photo",
                    created_by_id=created_by_id,
                )

            # Step 5: Upsert fv best practices
            best_practices: dict = payload.get("form", {}).get(
                "best_practice_questions", {}
            )

            if best_practices:
                for question, answer in best_practices.items():
                    if isinstance(answer, dict):
                        self.process_fv_best_practice(
                            raw_payload=raw_payload,
                            bp=question,
                            bp_payload=answer,
                            created_by_id=created_by_id,
                        )
                    else:
                        continue

            # Step 6: Upsert other fv questions and answers
            other_fv_questions: dict = payload.get("form", {})
            fv_questions = {}
            for question, answer in other_fv_questions.items():
                if question not in FV_QUESTIONS_IGNORE_LIST:
                    fv_questions.update({question: answer})
                elif "signature" in question:
                    image_url = (
                        payload.get("attachments", {})
                        .get(payload.get("form", {}).get(question, ""), {})
                        .get("url", "")
                    )
                    self.process_image(
                        image_url=image_url,
                        payload=payload,
                        image_reference_obj=result,
                        image_description=question,
                        created_by_id=created_by_id,
                    )
                else:
                    continue
            if fv_questions:
                self.process_fv_best_practice(
                    raw_payload=raw_payload,
                    bp="other",
                    bp_payload=fv_questions,
                    created_by_id=created_by_id,
                )

            # Step 7: Upsert FIS data
            fis_questions: dict = (
                payload.get("form", {})
                .get("field_inventory_survey", {})
                .get("general_plot_information")
            )

            if fis_questions:
                if isinstance(fis_questions, list):
                    for farm in fis_questions:
                        self.process_fis_farm(
                            raw_payload=raw_payload,
                            cleaned_payload=farm,
                            created_by_id=created_by_id,
                        )
                elif isinstance(fis_questions, dict):
                    self.process_fis_farm(
                        raw_payload=raw_payload,
                        cleaned_payload=farm,
                        created_by_id=created_by_id,
                    )

            # Step 8: Upsert Checks
            survey_detail = payload.get("form", {}).get("@name")
            if survey_detail == "Farm Visit - AA" and (
                (
                    payload.get("app_id", "") == "30cee26f064e403388e334ae7b0c403b"
                    and payload.get("metadata", {}).get("app_build_version", 0) >= 217
                )
                or (
                    payload.get("app_id", "") == "812728b8b35644dabb51561420938ee0"
                    and payload.get("metadata", {}).get("app_build_version", 0) >= 69
                )
            ):  # Testing for ONLY KENYA
                for farmer in ["farmer_1_questions", "farmer_2_questions"]:

                    # Process farmer 2 ONLY if the dictionary exists in form data
                    if farmer == "farmer_2_questions" and not payload.get(
                        "form", {}
                    ).get(farmer):
                        continue
                    cleaned_payload: dict = payload.get("form", {}).get(farmer, {})
                    self.process_check(
                        raw_payload=raw_payload,
                        cleaned_payload=cleaned_payload,
                        check_type="Farm Visit",
                        created_by_id=created_by_id,
                    )

            return result

        except ValueError as e:
            self.db.rollback()
            logger.error({"message": f"Value error in farm visit processing: {str(e)}"})
            raise

        except Exception as e:
            logger.error({f"Error processing farm visit: {str(e)}"})
            self.db.rollback()
            raise

    def process_fv_best_practice(
        self, raw_payload: dict, bp: str, bp_payload: dict, created_by_id: str
    ) -> FVBestPractice:
        """Complete workflow for processing fv best practice payload"""

        try:
            # Step 1: Parse raw JSON into Pydantic schema
            payload = raw_payload

            # Step 2: Transform payload (includes foreign key resolution)
            transformed_data = self.fv_best_practice_transformer.transform(payload, bp)

            # Step 3: Upsert to database
            result = self.fv_best_practice_service.upsert(
                transformed_data, created_by_id
            )

            logger.info({f"Upserted fv best practice with record ID: '{result.id}'"})

            # Step 4: Upsert the Best practice answers
            best_practice_answers: dict = bp_payload

            if best_practice_answers:
                for question, answer in best_practice_answers.items():
                    if any(word in question.lower() for word in ["photo", "image"]):
                        continue
                    elif question in FV_BP_MULTISELECT:
                        multiselect = answer.split(" ")
                        for ans in multiselect:
                            self.process_fv_best_practice_answers(
                                raw_payload=raw_payload,
                                bp=bp,
                                bp_question=question,
                                bp_answer=ans,
                                multiselect=True,
                                created_by_id=created_by_id,
                            )
                    else:
                        self.process_fv_best_practice_answers(
                            raw_payload=raw_payload,
                            bp=bp,
                            bp_question=question,
                            bp_answer=answer,
                            multiselect=False,
                            created_by_id=created_by_id,
                        )

            # Step 4: Upsert associated images if any
            if best_practice_answers:
                for question, answer in best_practice_answers.items():
                    if any(word in question.lower() for word in ["photo", "image"]):
                        image_url: str = (
                            raw_payload.get("attachments", {})
                            .get(answer, {})
                            .get("url", "")
                        )
                        if (
                            image_url.endswith(".jpg")
                            or image_url.endswith(".png")
                            or image_url.endswith(".heic")
                        ):
                            self.process_image(
                                image_url=image_url,
                                payload=raw_payload,
                                image_reference_obj=result,
                                image_description=question,
                                created_by_id=created_by_id,
                            )
                    else:
                        continue

            return result

        except ValueError as e:
            self.db.rollback()
            logger.error(
                {"message": f"Value error in fv best practice processing: {str(e)}"}
            )
            raise

        except Exception as e:
            logger.error({f"Error processing fv best practice: {str(e)}"})
            self.db.rollback()
            raise

    def process_fv_best_practice_answers(
        self,
        raw_payload: dict,
        bp: str,
        bp_question: str,
        bp_answer: str,
        multiselect: bool,
        created_by_id: str,
    ) -> FVBestPracticeAnswer:
        """Function to process the best practice answers"""
        try:
            # Step 1: Parse raw JSON into Pydantic schema
            payload = raw_payload

            # Step 2: Transform payload (includes foreign key resolution)
            transformed_data = self.fv_best_practice_answer_transformer.transform(
                payload, bp, bp_question, bp_answer, multiselect
            )

            # Step 3: Upsert to database
            result = self.fv_best_practice_answer_service.upsert(
                transformed_data, created_by_id
            )

            logger.info(
                {f"Upserted fv best practice answer with record ID: '{result.id}'"}
            )

            return result

        except ValueError as e:
            self.db.rollback()
            logger.error(
                {
                    "message": f"Value error in fv best practice answer processing: {str(e)}"
                }
            )
            raise

        except Exception as e:
            logger.error({f"Error processing fv best practice answer: {str(e)}"})
            self.db.rollback()
            raise

    def process_fis_farm(
        self, raw_payload: dict, cleaned_payload: dict, created_by_id: str
    ) -> Farm:
        """Function to process the FIS farm"""
        try:
            # Step 1: Transform payload (includes foreign key resolution)
            transformed_data = self.farm_transformer.transform(
                raw_payload, cleaned_payload
            )

            # Step 2: Upsert to database
            result = self.farm_service.upsert(transformed_data, created_by_id)

            # Step 3: Upsert Coffee Variety
            payload = cleaned_payload

            logger.info({f"Upserted FIS farm answer with record ID: '{result.id}'"})

            varieties = payload.get("varieties", "").split()
            if varieties:
                for variety in varieties:
                    cleaned_payload = {
                        "variety": variety,
                        "farm_submission_id": result.submission_id,
                        "number_of_trees": payload.get(f"variety_{variety}"),
                    }
                    self.process_fis_variety(
                        cleaned_payload=cleaned_payload, created_by_id=created_by_id
                    )

            # Step 4: Upsert images
            image_url = (
                raw_payload.get("attachments", {})
                .get(payload.get("plot_photo"))
                .get("url", "")
            )
            if image_url:
                self.process_image(
                    image_url=image_url,
                    payload=raw_payload,
                    image_reference_obj=result,
                    image_description="Farm Photo",
                    created_by_id=created_by_id,
                )

            return result

        except ValueError as e:
            self.db.rollback()
            logger.error({"message": f"Value error in FIS farm processing: {str(e)}"})
            raise

        except Exception as e:
            logger.error({f"Error processing FIS farm: {str(e)}"})
            self.db.rollback()
            raise

    def process_fis_variety(
        self, cleaned_payload: dict, created_by_id: str
    ) -> CoffeeVariety:
        """Function to process the FIS coffee varieties"""
        try:

            # Step 1: Transform payload (includes foreign key resolution)
            transformed_data = self.variety_transformer.transform(cleaned_payload)

            # Step 2: Upsert to database
            result = self.variety_service.upsert(transformed_data, created_by_id)

            logger.info({f"Upserted FIS variety with record ID: '{result.id}'"})

            return result

        except ValueError as e:
            self.db.rollback()
            logger.error(
                {"message": f"Value error in FIS variety processing: {str(e)}"}
            )
            raise

        except Exception as e:
            logger.error({f"Error processing FIS variety: {str(e)}"})
            self.db.rollback()
            raise

    def process_check(
        self,
        raw_payload: dict,
        cleaned_payload: dict,
        check_type: str,
        created_by_id: str,
    ) -> Check:
        """Function to process the FV checks"""
        try:

            # Step 1: Transform payload (includes foreign key resolution)
            transformed_data = self.check_transformer.transform(
                raw_payload=raw_payload,
                cleaned_payload=cleaned_payload,
                check_type=check_type,
            )

            # Step 2: Upsert to database
            result = self.check_service.upsert(transformed_data, created_by_id)

            logger.info({f"Upserted FV check with record ID: '{result.id}'"})

            return result

        except ValueError as e:
            self.db.rollback()
            logger.error({"message": f"Value error in FV  processing: {str(e)}"})
            raise

        except Exception as e:
            logger.error({f"Error processing FV check: {str(e)}"})
            self.db.rollback()
            raise

    def process_image(
        self,
        image_url: str,
        payload: dict,
        image_reference_obj: object,
        image_description: str,
        created_by_id: str,
    ) -> Image:
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
                        f"Upserted image with record ID: '{image_result.id}' for farm visit ID: '{image_reference_obj.id}'"
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
