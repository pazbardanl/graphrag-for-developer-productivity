import os
import threading
from services.data_driver import DataDriver
from services.processor import Processor
from services.graph_data_provider import GraphDataProvider

def __get_kafka_config():
    kafka_bootstrap_servers = os.environ["KAFKA_BOOTSTRAP_SERVERS"]
    new_pr_events_topic = os.environ["KAFKA_NEW_PR_EVENTS_TOPIC"]
    group_id = os.environ["KAFKA_REVIEWER_SCORING_SERVICE_GROUP_ID"]
    return kafka_bootstrap_servers, new_pr_events_topic, group_id

def __start_data_driver(kafka_bootstrap_servers, new_pr_events_topic, group_id, processor):
    data_driver = DataDriver(kafka_bootstrap_servers, new_pr_events_topic, group_id, processor)
    threading.Thread(target=data_driver.start, daemon=True).start()

def main():
    print("Reviewer Scoring service started")
    kafka_bootstrap_servers, new_pr_events_topic, group_id = __get_kafka_config()
    graph_data_provider = GraphDataProvider("http://graph-service:8000")
    processor = Processor(graph_data_provider)
    data_driver = DataDriver(kafka_bootstrap_servers, new_pr_events_topic, group_id, processor)
    data_driver.start()
    print("Reviewer Scoring service exited")

if __name__ == "__main__":
    main()