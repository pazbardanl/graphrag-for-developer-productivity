import networkx as nx
from confluent_kafka import Consumer
from services.data_driver import DataDriver
from services.processor import Processor

def main():
    print("Graph service started")
    processor = Processor()
    data_driver = DataDriver("kafka:9092", "PR_events", "gr-id-0", processor.process)
    data_driver.start()

if __name__ == "__main__":
    main()