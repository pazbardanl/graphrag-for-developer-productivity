import json
from typing import List
from datetime import datetime
from common.models.pr_event import PREventDto

class Processor:

    def process(self, json_string: str) -> list[PREventDto]:
        try:
            raw_events = json.loads(json_string)
        except json.JSONDecodeError as e:
            raise ValueError("Invalid JSON format") from e

        parsed = []
        for i, item in enumerate(raw_events):
            try:
                dto = self.__parse_event(item)
                parsed.append(dto)
            except KeyError as e:
                print(f"Missing expected key in event {i}: {e}")
            except Exception as e:
                print(f"Error parsing event {i}: {e}")
        return parsed
    
    def __parse_event(self, event_json: str) -> PREventDto:
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