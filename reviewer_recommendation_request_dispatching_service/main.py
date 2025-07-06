import os
import threading
from services.data_driver import DataDriver
from services.processor import Processor
from services.user_data_provider import UserDataProvider
from services.publisher import Publisher
from common.helpers.my_logger import MyLogger

logger = MyLogger().get_logger(__name__)

def _get_kafka_config():
    kafka_bootstrap_servers = os.environ["KAFKA_BOOTSTRAP_SERVERS"]
    new_pr_events_topic = os.environ["KAFKA_NEW_PR_EVENTS_TOPIC"]
    reviewer_recommendation_requests_openai = os.environ["KAFKA_REVIEWER_RECOMMENDATION_REQUESTS_OPENAI_TOPIC"]
    group_id = os.environ["KAFKA_REVIEWER_RECOMMENDATION_REQUEST_DISPATCHING_SERVICE_GROUP_ID"]
    return kafka_bootstrap_servers, new_pr_events_topic, reviewer_recommendation_requests_openai, group_id

def _start_data_driver(kafka_bootstrap_servers, new_pr_events_topic, group_id, processor):
    data_driver = DataDriver(kafka_bootstrap_servers, new_pr_events_topic, group_id, processor)
    data_driver.start()

def main():
    logger.info("started")
    kafka_bootstrap_servers, new_pr_events_topic, reviewer_recommendation_requests_openai, group_id = _get_kafka_config()
    user_data_provider = UserDataProvider("http://user-data-service:8000")
    reviewer_recommendation_request_openai_publisher = Publisher(kafka_bootstrap_servers, reviewer_recommendation_requests_openai)
    processor = Processor(user_data_provider, reviewer_recommendation_request_openai_publisher)
    _start_data_driver(kafka_bootstrap_servers, new_pr_events_topic, group_id, processor)
    logger.info("exited")

if __name__ == "__main__":
    main()