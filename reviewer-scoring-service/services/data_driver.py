from confluent_kafka import Consumer
from typing import Callable
from services.processor import Processor
import threading
import json
from common.helpers.my_logger import MyLogger

logger = MyLogger().get_logger(__name__)

class DataDriver:
    def __init__(self, kafka_bootstrap_servers: str, kafka_topic: str, group_id: str, processor: Processor):
        logger.info("initialized, listening to topic: %s", kafka_topic)
        self.kafka_topic = kafka_topic
        self.processor = processor
        self.consumer = Consumer({
            'bootstrap.servers': kafka_bootstrap_servers,
            'group.id': group_id,
            'auto.offset.reset': 'earliest'
        })

    def start(self):
        logger.info("started")
        self.consumer.subscribe([self.kafka_topic])
        try:
            logger.info("Consumer loop started")
            while True:
                msg = self.consumer.poll(timeout=1.0)
                if msg is None:
                    continue
                if msg.error():
                    print(f"Consumer error: {msg.error()}")
                    continue
                self.processor.process(msg.value().decode('utf-8'))
        except KeyboardInterrupt:
            logger.info("Consumer shutting down")
        finally:
            self.consumer.close()
            logger.info("Consumer closed")
        logger.info("exited")