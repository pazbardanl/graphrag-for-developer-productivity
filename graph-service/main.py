import networkx as nx
from confluent_kafka import Consumer
from services.data_provider import DataProvider
from services.processor import Processor

def main():
    print("Graph service started")
    processor = Processor()
    data_provider = DataProvider("kafka:9092", "PR_events", "gr-id-0", processor.process)
    data_provider.start()

if __name__ == "__main__":
    main()