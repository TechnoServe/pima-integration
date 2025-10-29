"""Init file for centralized services import"""

from .attendance import AttendanceService
from .farmer import FarmerService
from .household import HouseholdService
from .image import ImageService
from .observation_result import ObservationResultService
from .observation import ObservationService
from .resolvers import ForeignKeyResolver
from .training_session import TrainingSessionService
from .farm_visit import FarmVisitService
from .fv_best_practice import FVBestPracticeService
from .fv_best_practice_answer import FVBestPracticeAnswerService
from .skip_transformation import SkipTransformation
from .coffee_variety import CoffeeVarietyService
from .farm import FarmService
from .check import CheckService
from .wetmill_visit import WetmillVisitService
from .wv_survey_response import WVSurveyResponseService
from .wv_survey_question_response import WVSurveyQuestionResponseService
from .wetmill import WetmillService

print("Imported all services successfully!")
