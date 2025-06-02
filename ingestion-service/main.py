import json
import time
from services.data_provider import DataProvider
from services.processor import Processor
from services.publisher import Publisher
from common.models.pr_event import PREventDto

def main():
    print("Ingestion service started")
    dataProvider = DataProvider("mock_data/mock_github_events.json")
    processor = Processor()
    publisher = Publisher(kafka_bootstrap_servers="kafka:9092", kafka_topic="PR_events")
    json_string = dataProvider.provide()
    events = processor.process(json_string)
    for event in events:
        publisher.publish(event=event)
    print("Ingestion service exited")


if __name__ == "__main__":
    main()
