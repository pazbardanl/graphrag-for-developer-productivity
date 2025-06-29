import time
import json
import uuid
from confluent_kafka import Producer, Consumer
import pytest
from common.helpers.my_logger import MyLogger
from tests.integration.integ_test_utils import get_test_pr_events
from tests.integration.integ_test_utils import inject_input_pr_events
from tests.integration.integ_test_utils import capture_output_events
from typing import List
from common.models.pr_event import PREventDto

# TODO: put this in docker-compose.test.yml
INPUT_FILE_PATH = "tests/test_data/mock_github_events_4events_3prs.json"
INPUT_TOPIC = "test_PR_events"
OUTPUT_TOPIC = "test_PR_events"
KAFKA_BOOTSTRAP_SERVERS = "kafka:9092"
GROUP_ID = f"integ_test_group_{uuid.uuid4()}"
EXPECTED_OUTPUT_COUNT = 4
TIMEOUT_SECS = 10

logger = MyLogger().get_logger(__name__)
logger.propagate = False

def assert_on_output_events(output_events: List[dict]):
    expected_pr_numbers = [100, 200, 101]
    actual_pr_numbers = [event['pr_number'] for event in output_events]
    logger.debug(f'expected PR numbers: {expected_pr_numbers}, actual PR numbers: {actual_pr_numbers}')
    assert len(output_events) == EXPECTED_OUTPUT_COUNT, f"Expected {EXPECTED_OUTPUT_COUNT} messages, got {len(output_events)}"
    assert all(pr_number in actual_pr_numbers for pr_number in expected_pr_numbers), f"Expected PR numbers {expected_pr_numbers} not found in actual PR numbers {actual_pr_numbers}"

def test_runner_sanity_shortcircuit():
    logger.info(f"Reading test input events from: {INPUT_FILE_PATH}")
    input_pr_events = get_test_pr_events(INPUT_FILE_PATH)
    logger.info(f'Injecting {len(input_pr_events)} input PR events into {INPUT_TOPIC}...')
    inject_input_pr_events(input_pr_events, KAFKA_BOOTSTRAP_SERVERS, INPUT_TOPIC)
    logger.info(f'Waiting for {EXPECTED_OUTPUT_COUNT} messages on {OUTPUT_TOPIC}...')
    output_events = capture_output_events(KAFKA_BOOTSTRAP_SERVERS, OUTPUT_TOPIC, GROUP_ID, EXPECTED_OUTPUT_COUNT, TIMEOUT_SECS)
    logger.info(f'Asserting on {len(output_events)} messages captured from {OUTPUT_TOPIC}')
    assert_on_output_events(output_events)
    logger.info(f'Test completed successfully!')