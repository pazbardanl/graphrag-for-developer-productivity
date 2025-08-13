from common.helpers.my_logger import MyLogger
from services.pr_reviewer_selector import PRReviewerSelector
from services.publisher import Publisher
from common.models.pr_reviewer_recommendation import PRReviewerRecommendation
from common.models.pr_reviewer_recommendation_request import PrReviewerRecommendationRequest

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
        pr_reviewer_recommendation_request = PrReviewerRecommendationRequest.model_validate_json(json_string)
        if not pr_reviewer_recommendation_request:
            logger.error('PR reviewer recommendation request not provided (None or empty)')
            return
        logger.debug(f'Processing PR reviewer recommendation request: {pr_reviewer_recommendation_request}')
        try:
            recommendation = self.reviewer_selector.select(pr_reviewer_recommendation_request)
            if not recommendation:
                logger.info(f"No recommendation generated for PR {pr_reviewer_recommendation_request.pr_number}")
                return
            logger.info(f"PR number : {recommendation.pr_number}, Recommended reviewer: {recommendation.recommended_reviewer}") 
            self.publisher.publish(recommendation)
        except Exception as e:
            logger.error(f"Failed to get reviewer recommendation: {e}", exc_info=True)
