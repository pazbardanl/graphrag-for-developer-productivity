import networkx as nx
import os
from confluent_kafka import Consumer
from services.data_driver import DataDriver
from services.processor import Processor
from services.publisher import Publisher

def main():
    print("Graph service started")
    kafka_bootstrap_servers = os.environ["KAFKA_BOOTSTRAP_SERVERS"]
    pr_events_topic = os.environ["KAFKA_PR_EVENTS_TOPIC"]
    new_pr_events_topic = os.environ["KAFKA_NEW_PR_EVENTS_TOPIC"]
    group_id = os.environ["KAFKA_GROUP_ID"]

    new_pr_events_publisher = Publisher(kafka_bootstrap_servers, new_pr_events_topic)
    processor = Processor(new_pr_events_publisher)
    data_driver = DataDriver(kafka_bootstrap_servers, pr_events_topic, group_id, processor)
    data_driver.start()

if __name__ == "__main__":
    main()