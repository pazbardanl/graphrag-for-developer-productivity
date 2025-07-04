import os
import threading
from services.data_driver import DataDriver
from services.processor import Processor
from common.helpers.my_logger import MyLogger
from services.openai_pr_reviewer_selector import OpenAIPrReviewerSelector
from services.pr_reviewer_selector import PRReviewerSelector
from services.publisher import Publisher

logger = MyLogger().get_logger(__name__)

def _get_kafka_config():
    kafka_bootstrap_servers = os.environ["KAFKA_BOOTSTRAP_SERVERS"]
    reviewer_report_topic = os.environ["KAFKA_REVIEWER_REPORT_TOPIC"]
    reviewer_recommendation_topic = os.environ["KAFKA_REVIEWER_RECOMMENDATION_TOPIC"]
    group_id = os.environ["KAFKA_REVIEWER_RECOMMENDATION_SERVICE_GROUP_ID"]
    return kafka_bootstrap_servers, reviewer_report_topic, reviewer_recommendation_topic, group_id

def _start_data_driver(kafka_bootstrap_servers, reviewer_report_topic, group_id, processor):
    data_driver = DataDriver(kafka_bootstrap_servers, reviewer_report_topic, group_id, processor)
    data_driver.start()

def main():
    logger.info("started")
    kafka_bootstrap_servers, reviewer_report_topic, reviewer_recommendation_topic, group_id = _get_kafka_config()
    reviewer_selector: PRReviewerSelector = OpenAIPrReviewerSelector()
    publisher = Publisher(kafka_bootstrap_servers, reviewer_recommendation_topic)
    processor = Processor(reviewer_selector, publisher)
    _start_data_driver(kafka_bootstrap_servers, reviewer_report_topic, group_id, processor)
    logger.info("exited")

if __name__ == "__main__":
    main()