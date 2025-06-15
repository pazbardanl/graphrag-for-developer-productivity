from common.helpers.my_logger import MyLogger
from services.pr_reviewer_selector import PRReviewerSelector
from services.publisher import Publisher
from common.models.pr_reviewer_recommendation import PRReviewerRecommendation
from common.models.pr_reviewers_report import PRReviewerReport

logger = MyLogger().get_logger(__name__)

class Processor:
    def __init__(self, reviewer_selector: PRReviewerSelector, publisher: Publisher):
        self.reviewer_selector = reviewer_selector
        self.publisher = publisher
        logger.info("initialized")

    def process(self, json_string: str):
        logger.debug(f'incoming: {json_string}')
        if not json_string:
            logger.error('Empty JSON string provided')
            return
        pr_reviewer_report = PRReviewerReport.model_validate_json(json_string)
        if not pr_reviewer_report:
            logger.error('PR reviewer report not provided')
            return
        logger.debug(f'Processing PR reviewer report: {pr_reviewer_report}')
        try:
            recommendation = self.reviewer_selector.select(pr_reviewer_report)
            if not recommendation:
                logger.info(f"No recommendation generated for PR {pr_reviewer_report.pr_number}")
                return
            logger.debug(f"Recommendation: {recommendation}")
            self.publisher.publish(recommendation)
        except Exception as e:
            logger.error(f"Failed to get reviewer recommendation: {e}", exc_info=True)
