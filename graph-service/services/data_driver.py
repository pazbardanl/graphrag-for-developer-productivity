from confluent_kafka import Consumer
from typing import Callable
import threading
import json

class DataDriver:
    def __init__(self, kafka_bootstrap_servers: str, kafka_topic: str, group_id: str, processor_callback: Callable[[dict], None]):
        self.kafka_topic = kafka_topic
        self.processor_callback = processor_callback
        self.consumer = Consumer({
            'bootstrap.servers': kafka_bootstrap_servers,
            'group.id': group_id,
            'auto.offset.reset': 'earliest'
        })

    def start(self):
        print("Starting Kafka consumer loop..." ,flush=True)
        self.consumer.subscribe([self.kafka_topic])
        try:
            while True:
                msg = self.consumer.poll(timeout=1.0)
                if msg is None:
                    continue
                if msg.error():
                    print(f"Consumer error: {msg.error()}")
                    continue
                self.processor_callback(msg.value())
        except KeyboardInterrupt:
            print("Consumer shutting down", flush=True)
        finally:
            self.consumer.close()