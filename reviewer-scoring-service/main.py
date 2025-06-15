import os
import threading
from services.data_driver import DataDriver
from services.processor import Processor
from services.graph_data_provider import GraphDataProvider
from services.publisher import Publisher
from common.helpers.my_logger import MyLogger

logger = MyLogger().get_logger(__name__)

def _get_kafka_config():
    kafka_bootstrap_servers = os.environ["KAFKA_BOOTSTRAP_SERVERS"]
    new_pr_events_topic = os.environ["KAFKA_NEW_PR_EVENTS_TOPIC"]
    reviewer_report_topic = os.environ["KAFKA_REVIEWER_REPORT_TOPIC"]
    group_id = os.environ["KAFKA_REVIEWER_SCORING_SERVICE_GROUP_ID"]
    return kafka_bootstrap_servers, new_pr_events_topic, reviewer_report_topic, group_id

def _start_data_driver(kafka_bootstrap_servers, new_pr_events_topic, group_id, processor):
    data_driver = DataDriver(kafka_bootstrap_servers, new_pr_events_topic, group_id, processor)
    data_driver.start()

def main():
    logger.info("started")
    kafka_bootstrap_servers, new_pr_events_topic, reviewer_report_topic, group_id = _get_kafka_config()
    graph_data_provider = GraphDataProvider("http://graph-service:8000")
    reviewer_report_publisher = Publisher(kafka_bootstrap_servers, reviewer_report_topic)
    processor = Processor(graph_data_provider, reviewer_report_publisher)
    _start_data_driver(kafka_bootstrap_servers, new_pr_events_topic, group_id, processor)
    logger.info("exited")

if __name__ == "__main__":
    main()