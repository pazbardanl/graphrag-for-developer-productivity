from common.helpers.my_logger import MyLogger
from services.pr_reviewer_selector import PRReviewerSelector
from services.publisher import Publisher
from common.models.pr_reviewer_recommendation import PRReviewerRecommendation
from common.models.pr_event import PREventDto

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
        pr_event = PREventDto.model_validate_json(json_string)
        if not pr_event:
            logger.error('PR event not provided (None or empty)')
            return
        logger.debug(f'Processing PR event: {pr_event}')
        try:
            recommendation = self.reviewer_selector.select(pr_event)
            if not recommendation:
                logger.info(f"No recommendation generated for PR {pr_event.pr_number}")
                return
            logger.debug(f"Recommendation: {recommendation}")
            self.publisher.publish(recommendation)
        except Exception as e:
            logger.error(f"Failed to get reviewer recommendation: {e}", exc_info=True)
