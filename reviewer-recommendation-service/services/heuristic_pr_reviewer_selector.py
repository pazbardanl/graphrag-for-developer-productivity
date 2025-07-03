from services.pr_reviewer_selector import PRReviewerSelector
from common.models.pr_reviewer_recommendation import PRReviewerRecommendation
from common.models.pr_reviewers_report import PRReviewerReport
from common.helpers.my_logger import MyLogger

logger = MyLogger().get_logger(__name__)

class HeuristicPRReviewerSelector(PRReviewerSelector):
    def select(self, pr_event: PREventDto) -> PRReviewerRecommendation:
        pass