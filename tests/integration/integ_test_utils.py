import time
from datetime import datetime
import json
from typing import List, Dict, Any 
from confluent_kafka import Producer, Consumer
from common.helpers.my_logger import MyLogger
from common.models.pr_event import PREventDto

logger = MyLogger().get_logger(__name__)

def inject_input_pr_events(pr_events: List[PREventDto], kafka_bootstrap_servers:str, input_topic:str):
    kafka_producer = _get_kafka_producer(kafka_bootstrap_servers)
    for event in pr_events:
        kafka_producer.produce(topic=input_topic, value=event.model_dump_json().encode("utf-8"), callback=_kafka_delivery_report)
    kafka_producer.flush()

def capture_output_events(kafka_bootstrap_servers:str, output_topic:str, group_id: str, expected_output_count: int, timeout_secs: int) -> List[dict]:
    kafka_consumer = _get_kafka_consumer(kafka_bootstrap_servers, output_topic, group_id)
    output_events = []
    start_time = time.time()
    try:
        while len(output_events) < expected_output_count and (time.time() - start_time) < timeout_secs:
            msg = kafka_consumer.poll(1.0)
            if msg is not None and not msg.error():
                output_events.append(json.loads(msg.value().decode("utf-8")))
        return output_events
    finally:
        kafka_consumer.close()

def get_test_pr_events(json_file_path: str)-> List[PREventDto]:
    list_of_dicts = _read_json_file_as_list(json_file_path)
    raw_events = [_parse_pr_event(item) for item in list_of_dicts]
    return raw_events

def _kafka_delivery_report(err, msg):
        if err is not None:
            logger.error(f"Message delivery failed: {err}")

def _get_kafka_producer(kafka_bootstrap_servers: str) -> Producer:
    producer = Producer({'bootstrap.servers': kafka_bootstrap_servers})
    return producer

def _get_kafka_consumer(kafka_bootstrap_servers: str, kafka_topic:str, group_id: str) -> Consumer:
    consumer = Consumer({
            'bootstrap.servers': kafka_bootstrap_servers,
            'group.id': group_id,
            'auto.offset.reset': 'earliest'
    })
    consumer.subscribe([kafka_topic])
    return consumer

def _read_json_file_as_list(json_file_path: str) -> List[Dict[str, Any]]:
    with open(json_file_path, "r", encoding="utf-8") as file:
        return json.load(file)

def _parse_pr_event(event_json: dict) -> PREventDto:
        action = event_json["action"]
        repo_name = event_json["repository"]["full_name"]
        sender = event_json["sender"]["login"]
        
        pr = event_json["pull_request"]
        pr_number = pr["number"]
        pr_user = pr["user"]["login"]
        pr_files_changed = pr.get("changed_files", [])

        review = event_json.get("review", [])
        review_user = None
        review_state = None
        review_submitted_at = None
        if review:
            review_user = review["user"]["login"]
            review_state = review["state"]
            review_submitted_at =  datetime.strptime(review["submitted_at"], "%Y-%m-%dT%H:%M:%SZ")

        dto = PREventDto(
            action=action,
            repo_name=repo_name,
            sender=sender,
            pr_number=pr_number,
            pr_user=pr_user,
            pr_files_changed=pr_files_changed,
            review_user  = review_user,
            review_state = review_state,
            review_submitted_at = review_submitted_at
        )
        return dto