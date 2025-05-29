from confluent_kafka import Producer
from models.pr_event import PREventDto

class Publisher:
    def __init__(self, kafka_bootstrap_servers: str, kafka_topic:str):
        self.producer = Producer({'bootstrap.servers': kafka_bootstrap_servers})
        self.topic = kafka_topic

    def delivery_report(self, err, msg):
        if err is not None:
            print(f"Message delivery failed: {err}")
        else:
            print(f"Message delivered to {msg.topic()} [{msg.partition()}]")
    
    def publish(self, event: PREventDto):
        try:
            payload = event.model_dump_json()
            self.producer.produce(
                topic=self.topic,
                value=payload,
                callback=self.delivery_report
            )
            print(f"Message delivered: {payload}")
            self.producer.poll(0)  # Trigger delivery callback
        except Exception as e:
            print(f"Failed to produce message: {e}")

    def flush(self):
        self.producer.flush()