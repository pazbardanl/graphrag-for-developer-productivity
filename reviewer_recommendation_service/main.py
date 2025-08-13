import os
import threading
from services.data_driver import DataDriver
from services.processor import Processor
from common.helpers.my_logger import MyLogger
from services.openai_pr_reviewer_selector import OpenAIPrReviewerSelector
from services.heuristic_pr_reviewer_selector import HeuristicPRReviewerSelector
from services.pr_reviewer_selector import PRReviewerSelector
from common.helpers.graph_data_provider import GraphDataProvider
from services.publisher import Publisher

logger = MyLogger().get_logger(__name__)

OPENAI_PR_REVIEWER_SELECTOR_TYPE = "openai_pr_reviewer_selector"
HEURISTIC_PR_REVIEWER_SELECTOR_TYPE = "heuristic_pr_reviewer_selector"

def _get_kafka_config():
    kafka_bootstrap_servers = os.environ["KAFKA_BOOTSTRAP_SERVERS"]
    reviewer_recommendation_request_topic = _get_reviewer_recommendation_requests_topic()
    reviewer_recommendation_topic = os.environ["KAFKA_REVIEWER_RECOMMENDATION_TOPIC"]
    group_id = os.environ["KAFKA_REVIEWER_RECOMMENDATION_SERVICE_GROUP_ID"]
    return kafka_bootstrap_servers, reviewer_recommendation_request_topic, reviewer_recommendation_topic, group_id

def _get_reviewer_recommendation_requests_topic():
    selector_type = os.getenv("PR_REVIEWER_SELECTOR", "openai_pr_reviewer_selector")
    if selector_type == OPENAI_PR_REVIEWER_SELECTOR_TYPE:
        return os.environ["KAFKA_REVIEWER_RECOMMENDATION_REQUESTS_OPENAI_TOPIC"]
    elif selector_type == HEURISTIC_PR_REVIEWER_SELECTOR_TYPE:
        return os.environ.get("KAFKA_REVIEWER_RECOMMENDATION_REQUESTS_HEURISTIC_TOPIC")
    else:
        raise ValueError(f"Unknown PR_REVIEWER_SELECTOR: {selector_type}")

def _get_pr_reviewer_selector(graph_data_provider: GraphDataProvider):
    selector_type = os.getenv("PR_REVIEWER_SELECTOR", "openai_pr_reviewer_selector")
    logger.info(f"Reviewer selector type = {selector_type}")
    if selector_type == OPENAI_PR_REVIEWER_SELECTOR_TYPE:
        return OpenAIPrReviewerSelector(graph_data_provider)
    elif selector_type == HEURISTIC_PR_REVIEWER_SELECTOR_TYPE:
        return HeuristicPRReviewerSelector(graph_data_provider)
    else:
        raise ValueError(f"Unknown PR_REVIEWER_SELECTOR: {selector_type}")

def _start_data_driver(kafka_bootstrap_servers, new_pr_events_topic, group_id, processor):
    data_driver = DataDriver(kafka_bootstrap_servers, new_pr_events_topic, group_id, processor)
    data_driver.start()

def main():
    logger.info("started")
    kafka_bootstrap_servers, reviewer_recommendation_request_topic, reviewer_recommendation_topic, group_id = _get_kafka_config()
    graph_data_provider = GraphDataProvider("http://graph-service:8000")
    reviewer_selector: PRReviewerSelector = _get_pr_reviewer_selector(graph_data_provider)
    publisher = Publisher(kafka_bootstrap_servers, reviewer_recommendation_topic)
    processor = Processor(reviewer_selector, publisher)
    _start_data_driver(kafka_bootstrap_servers, reviewer_recommendation_request_topic, group_id, processor)
    logger.info("exited")

if __name__ == "__main__":
    main()