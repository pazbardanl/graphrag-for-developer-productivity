from common.helpers.my_logger import MyLogger
from services.user_data_provider import UserDataProvider
from services.publisher import Publisher
from common.models.pr_event import PREventDto
from common.models.pr_reviewer_recommendation_request import PrReviewerRecommendationRequest
from common.models.selection_strategy import SelectionStrategy

logger = MyLogger().get_logger(__name__)

class Processor:
    # processor = Processor(user_data_provider, reviewer_recommendation_request_openai_publisher)
    def __init__(self, user_data_provider: UserDataProvider, reviewer_recommendation_request_openai_publisher: Publisher):
        self.user_data_provider = user_data_provider
        self.reviewer_recommendation_request_openai_publisher = reviewer_recommendation_request_openai_publisher
        logger.info("initialized")

    def process(self, json_string: str):
        logger.debug(f'incoming: {json_string}')
        if not json_string:
            logger.error('Empty JSON string provided')
            return
        pr_event = PREventDto.model_validate_json(json_string)
        if not pr_event:
            logger.error('New PR event not provided (None or empty)')
            return
        logger.debug(f'Incoming new PR event: {pr_event}')
        if pr_event.pr_number is None:
            logger.error('PR number not provided in the PR event. reviewer recommendation request not published')
            return
        if not pr_event.repo_name:
            logger.error('Repo name not provided in the PR event. reviewer recommendation request not published')
            return
        repo_name = pr_event.repo_name
        pr_number = pr_event.pr_number
        selection_strategy = self.user_data_provider.get_repo_reviewer_selection_strategy(repo_name)
        if not selection_strategy or selection_strategy == SelectionStrategy.UNDETERMINED:
            logger.warning(f"Undetermined selection strategy for repo {repo_name}, defaulting to {SelectionStrategy.HEURISTIC}")
            selection_strategy = SelectionStrategy.HEURISTIC
        logger.info(f"selection_strategy chosen: {selection_strategy}")
        pr_reviewer_recommendation_request = PrReviewerRecommendationRequest(
            pr_number=pr_number,
            repo_name=repo_name,
            selection_strategy=selection_strategy
        )
        match selection_strategy:
            case SelectionStrategy.OPENAI:
                self.reviewer_recommendation_request_openai_publisher.publish(pr_reviewer_recommendation_request)
            case SelectionStrategy.HEURISTIC | _:
                logger.error(f"unable to conclude selection strategy ({selection_strategy}), reviewer recommendation request not published")