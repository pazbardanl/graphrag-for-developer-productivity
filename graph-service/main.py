import networkx as nx
import uvicorn
import os
import threading
from confluent_kafka import Consumer
from services.data_driver import DataDriver
from services.processor import Processor
from services.publisher import Publisher
from services.graph_api import GraphAPI
from services.graph_wrapper import GraphWrapper

def __get_kafka_config():
    kafka_bootstrap_servers = os.environ["KAFKA_BOOTSTRAP_SERVERS"]
    pr_events_topic = os.environ["KAFKA_PR_EVENTS_TOPIC"]
    new_pr_events_topic = os.environ["KAFKA_NEW_PR_EVENTS_TOPIC"]
    group_id = os.environ["KAFKA_GROUP_ID"]
    return kafka_bootstrap_servers, pr_events_topic, new_pr_events_topic, group_id

def __start_data_driver(kafka_bootstrap_servers, pr_events_topic, group_id, processor):
    data_driver = DataDriver(kafka_bootstrap_servers, pr_events_topic, group_id, processor)
    threading.Thread(target=data_driver.start, daemon=True).start()

def __start_graph_api(graph_wrapper: GraphWrapper):
    api = GraphAPI(graph_wrapper)
    uvicorn.run(api.app, host="0.0.0.0", port=8000)

def main():
    print("Graph service started")
    kafka_bootstrap_servers, pr_events_topic, new_pr_events_topic, group_id = __get_kafka_config()
    graph = nx.MultiDiGraph()
    graph_wrapper = GraphWrapper(graph)
    new_pr_events_publisher = Publisher(kafka_bootstrap_servers, new_pr_events_topic)
    processor = Processor(graph_wrapper, new_pr_events_publisher)
    __start_data_driver(kafka_bootstrap_servers, pr_events_topic, group_id, processor)
    __start_graph_api(graph_wrapper)

if __name__ == "__main__":
    main()