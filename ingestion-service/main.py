import os
import json
import time
import logging
from services.data_provider import DataProvider
from services.processor import Processor
from services.publisher import Publisher
from common.models.pr_event import PREventDto
from common.helpers.my_logger import MyLogger

logger = MyLogger().get_logger(__name__)

def main():
    logger.info("started")
    mock_data_path = os.environ.get("MOCK_DATA_PATH", "mock_data/mock_github_events.json")
    kafka_bootstrap_servers = os.environ["KAFKA_BOOTSTRAP_SERVERS"]
    pr_events_topic = os.environ["KAFKA_PR_EVENTS_TOPIC"]

    dataProvider = DataProvider(mock_data_path)
    processor = Processor()
    publisher = Publisher(kafka_bootstrap_servers=kafka_bootstrap_servers, kafka_topic=pr_events_topic)
    json_string = dataProvider.provide()
    events = processor.process(json_string)
    for event in events:
        publisher.publish(event=event)
    logger.info("exited")

if __name__ == "__main__":
    main()
