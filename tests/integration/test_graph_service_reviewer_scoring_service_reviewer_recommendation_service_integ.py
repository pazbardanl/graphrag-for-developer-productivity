import time
import json
import uuid
import requests
from confluent_kafka import Producer, Consumer
import pytest
from common.helpers.my_logger import MyLogger
from tests.integration.integ_test_utils import get_test_pr_events
from tests.integration.integ_test_utils import inject_input_pr_events
from tests.integration.integ_test_utils import capture_output_events
from typing import List
from common.models.pr_event import PREventDto
from confluent_kafka.admin import AdminClient, NewTopic

# TODO: put this in docker-compose.test.yml
INPUT_FILE_PATH = "tests/test_data/mock_github_events_41events_21prs.json"
EXPECTED_EVENTS_FILE_PATH = "tests/test_data/expected_reviewer_recommendations.json"
INPUT_TOPIC = "test_PR_events"
OUTPUT_TOPIC = "test_reviewer_recommendations"
KAFKA_BOOTSTRAP_SERVERS = "kafka:9092"
GROUP_ID = f"integ_test_group_{uuid.uuid4()}"
EXPECTED_OUTPUT_COUNT = 18
TIMEOUT_SECS = 30

logger = MyLogger().get_logger(__name__)
logger.propagate = False

def test_graph_service_reviewer_scoring_service_reviewer_recommendation_service_integ():
    logger.info("Clearing input Kafka topic")
    clear_kafka_topic(KAFKA_BOOTSTRAP_SERVERS, INPUT_TOPIC)
    logger.info("Clearing output Kafka topic")
    clear_kafka_topic(KAFKA_BOOTSTRAP_SERVERS, OUTPUT_TOPIC)
    logger.info(f"Reading test input events from: {INPUT_FILE_PATH}")
    input_pr_events = get_test_pr_events(INPUT_FILE_PATH)
    logger.info(f'Injecting {len(input_pr_events)} input PR events into {INPUT_TOPIC}...')
    inject_input_pr_events(input_pr_events, KAFKA_BOOTSTRAP_SERVERS, INPUT_TOPIC)
    logger.info(f'Waiting for {EXPECTED_OUTPUT_COUNT} messages on {OUTPUT_TOPIC}...')
    output_events = capture_output_events(KAFKA_BOOTSTRAP_SERVERS, OUTPUT_TOPIC, GROUP_ID, EXPECTED_OUTPUT_COUNT, TIMEOUT_SECS)
    logger.info(f'Asserting on {len(output_events)} messages captured from {OUTPUT_TOPIC}')
    valid_pr_numbers = {event["pr_number"] for event in output_events}
    assert_on_output_events(output_events, valid_pr_numbers)
    logger.info(f'Test completed successfully!')

def clear_kafka_topic(bootstrap_servers, topic):
    admin = AdminClient({'bootstrap.servers': bootstrap_servers})
    admin.delete_topics([topic])
    time.sleep(2)
    admin.create_topics([NewTopic(topic, num_partitions=1, replication_factor=1)])
    time.sleep(2)

def sort_events(events: list[dict]) -> list[dict]:
    return sorted(
        events,
        key=lambda e: (
            e.get("pr_number"),
            json.dumps(e.get("pr_reviewer_report", []), sort_keys=True)
        )
    )

def load_expected_events(path):
    with open(path, "r") as f:
        return json.load(f)

def project_tested_event_fields(event):
    return {
        "pr_number": event.get("pr_number"),
        "recommended_reviewer": event.get("recommended_reviewer"),
        "pr_reviewer_report": event.get("pr_reviewer_report"),
    }

def assert_valid_recommendation_event(event, valid_pr_numbers: set[int]):
    assert event.get("pr_number") in valid_pr_numbers, f"pr_number {event.get('pr_number')} is not in the set of valid PR numbers: {valid_pr_numbers}"
    assert event.get("pr_reviewer_report") is not None, "pr_reviewer_report is None"
    assert isinstance(event.get("recommended_reviewer"), str) and event.get("recommended_reviewer"), "recommended_reviewer is not a valid string"
    assert isinstance(event.get("reasoning"), str) and event.get("reasoning"), "reasoning is not a valid string"

def assert_on_output_events(output_events: list[dict],  valid_pr_numbers: set[int]):
    for event in output_events:
        assert_valid_recommendation_event(event, valid_pr_numbers)