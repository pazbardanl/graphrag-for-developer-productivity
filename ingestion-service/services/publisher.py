from confluent_kafka import Producer
from common.models.pr_event import PREventDto
from common.helpers.my_logger import MyLogger

logger = MyLogger().get_logger(__name__)

class Publisher:
    def __init__(self, kafka_bootstrap_servers: str, kafka_topic:str):
        logger.info("initialized, publishing to Kafka topic: %s", kafka_topic)
        self.producer = Producer({'bootstrap.servers': kafka_bootstrap_servers})
        self.topic = kafka_topic

    def delivery_report(self, err, msg):
        if err is not None:
            logger.error(f"Message delivery failed: {err}")
    
    def publish(self, event: PREventDto):
        try:
            payload = event.model_dump_json()
            self.producer.produce(topic=self.topic, value=payload, callback=self.delivery_report)
            self.producer.flush()
        except Exception as e:
            logger.error(f"Failed to produce message: {e}")

    def flush(self):
        self.producer.flush()