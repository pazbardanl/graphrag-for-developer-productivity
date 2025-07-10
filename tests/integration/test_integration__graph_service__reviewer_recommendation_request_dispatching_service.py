import time
import json
import uuid
from confluent_kafka import Producer, Consumer
import pytest
from common.helpers.my_logger import MyLogger
from tests.integration.integ_test_utils import get_test_pr_events
from tests.integration.integ_test_utils import inject_input_pr_events
from tests.integration.integ_test_utils import capture_output_events
from tests.integration.integ_test_utils import get_events_as_list_of_dicts
from typing import List
from common.models.pr_event import PREventDto
from confluent_kafka.admin import AdminClient, NewTopic

# TODO: put this in docker-compose.test.yml
INPUT_FILE_PATH = "tests/test_data/mock_github_events_4events_3prs.json"
EXPECTED_OUTPUT_FILE_PATH = "tests/test_data/expected_reviewer_recommendation_requests_3requests.json"
INPUT_TOPIC = "test_PR_events"
OUTPUT_TOPIC = "test_reviewer_recommendation_requests_openai"
KAFKA_BOOTSTRAP_SERVERS = "kafka:9092"
GROUP_ID = f"integ_test_group_{uuid.uuid4()}"
EXPECTED_OUTPUT_COUNT = 3
TIMEOUT_SECS = 60

logger = MyLogger().get_logger(__name__)
logger.propagate = False

def assert_on_output_events(output_events: List[dict]):
    logger.debug(f'output_events: {output_events}')
    expeced_reviewer_recommendation_requests = get_events_as_list_of_dicts(EXPECTED_OUTPUT_FILE_PATH)
    assert len(output_events) == EXPECTED_OUTPUT_COUNT, f"Expected {EXPECTED_OUTPUT_COUNT} messages, got {len(output_events)}"
    def sort_key(event):
        return event["pr_number"]
    sorted_actual = sorted(output_events, key=sort_key)
    sorted_expected = sorted(expeced_reviewer_recommendation_requests, key=sort_key)
    assert sorted_actual == sorted_expected, f"Output events do not match expected events.\nExpected: {sorted_expected}\nActual: {sorted_actual}"

# TODO: extract this to a common utility file
def clear_kafka_topic(bootstrap_servers, topic):
    admin = AdminClient({'bootstrap.servers': bootstrap_servers})
    admin.delete_topics([topic])
    time.sleep(2)
    admin.create_topics([NewTopic(topic, num_partitions=1, replication_factor=1)])
    time.sleep(2)

def test_component_reviewer_recommendation_request_dispatching_service():
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
    assert_on_output_events(output_events)
    logger.info(f'Test completed successfully!')