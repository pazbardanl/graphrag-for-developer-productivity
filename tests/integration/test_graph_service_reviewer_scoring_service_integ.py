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

# TODO: put this in docker-compose.test.yml
INPUT_FILE_PATH = "tests/test_data/mock_github_events_41events_21prs.json"
EXPECTED_EVENTS_FILE_PATH = "tests/test_data/expected_reviewer_reports.json"
INPUT_TOPIC = "test_PR_events"
OUTPUT_TOPIC = "test_reviewer_reports"
KAFKA_BOOTSTRAP_SERVERS = "kafka:9092"
GROUP_ID = f"integ_test_group_{uuid.uuid4()}"
EXPECTED_OUTPUT_COUNT = 21
TIMEOUT_SECS = 10

logger = MyLogger().get_logger(__name__)
logger.propagate = False

def test_graph_service_new_pr_events():
    logger.info(f"Reading test input events from: {INPUT_FILE_PATH}")
    input_pr_events = get_test_pr_events(INPUT_FILE_PATH)
    logger.info(f'Injecting {len(input_pr_events)} input PR events into {INPUT_TOPIC}...')
    inject_input_pr_events(input_pr_events, KAFKA_BOOTSTRAP_SERVERS, INPUT_TOPIC)
    logger.info(f'Waiting for {EXPECTED_OUTPUT_COUNT} messages on {OUTPUT_TOPIC}...')
    output_events = capture_output_events(KAFKA_BOOTSTRAP_SERVERS, OUTPUT_TOPIC, GROUP_ID, EXPECTED_OUTPUT_COUNT, TIMEOUT_SECS)
    logger.info(f'Asserting on {len(output_events)} messages captured from {OUTPUT_TOPIC}')
    assert_on_output_events(output_events)
    logger.info(f'Test completed successfully!')

def sort_events(events: list[dict]) -> list[dict]:
    return sorted(
        events,
        key=lambda e: (
            e.get("pr_number"),
            json.dumps(e.get("reviewer_scores", []), sort_keys=True)
        )
    )

def load_expected_events(path):
    with open(path, "r") as f:
        return json.load(f)

def assert_on_output_events(output_events: List[dict]):
    logger.debug(f'actual output events: {output_events}')
    if not output_events:
        raise AssertionError("No output events captured from the output topic.")
    expected_events = load_expected_events(EXPECTED_EVENTS_FILE_PATH)
    logger.info(f'loaded {len(expected_events)} expected events from {EXPECTED_EVENTS_FILE_PATH}')
    assert len(output_events) == len(expected_events), f"Expected {len(expected_events)} output events, but got {len(output_events)}"
    sorted_actual = sort_events(output_events)
    sorted_expected = sort_events(expected_events)
    assert sorted_actual == sorted_expected, f"Output events do not match expected events.\nExpected: {sorted_expected}\nActual: {sorted_actual}"
    logger.info("Output events match expected events.")
    

# def test_graph_service_new_pr_events():
#     logger.info(f"Reading test input events from: {INPUT_FILE_PATH}")
#     input_pr_events = get_test_pr_events(INPUT_FILE_PATH)
#     logger.info(f'Injecting {len(input_pr_events)} input PR events into {INPUT_TOPIC}...')
#     inject_input_pr_events(input_pr_events, KAFKA_BOOTSTRAP_SERVERS, INPUT_TOPIC)
#     logger.info(f'Waiting for {EXPECTED_OUTPUT_COUNT} messages on {OUTPUT_TOPIC}...')
#     output_events = capture_output_events(KAFKA_BOOTSTRAP_SERVERS, OUTPUT_TOPIC, GROUP_ID, EXPECTED_OUTPUT_COUNT, TIMEOUT_SECS)
#     logger.info(f'Asserting on {len(output_events)} messages captured from {OUTPUT_TOPIC}')
#     assert_on_output_events(output_events)
#     logger.info(f'Test completed successfully!')