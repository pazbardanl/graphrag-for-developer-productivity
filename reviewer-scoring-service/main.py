import networkx as nx
import uvicorn
import os
import threading
from confluent_kafka import Consumer
from services.data_driver import DataDriver
from services.processor import Processor

def __get_kafka_config():
    kafka_bootstrap_servers = os.environ["KAFKA_BOOTSTRAP_SERVERS"]
    new_pr_events_topic = os.environ["KAFKA_NEW_PR_EVENTS_TOPIC"]
    group_id = os.environ["KAFKA_GROUP_ID"]
    return kafka_bootstrap_servers, new_pr_events_topic, group_id

def __start_data_driver(kafka_bootstrap_servers, new_pr_events_topic, group_id, processor):
    data_driver = DataDriver(kafka_bootstrap_servers, new_pr_events_topic, group_id, processor)
    threading.Thread(target=data_driver.start, daemon=True).start()

def main():
    print("Reviewer Scoring service started")
    kafka_bootstrap_servers, new_pr_events_topic, group_id = __get_kafka_config()
    processor = Processor()
    __start_data_driver(kafka_bootstrap_servers, new_pr_events_topic, group_id, processor)

if __name__ == "__main__":
    main()