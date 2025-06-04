import networkx as nx
from common.models.pr_event import PREventDto
from services.publisher import Publisher

class Processor:
    def __init__(self):
        self.graph = nx.DiGraph()
        self.new_pr_event_publisher = Publisher(kafka_bootstrap_servers="kafka:9092", kafka_topic="new_PR_events")
    
    def process(self, json_string: str):
        try:
            pr_event = PREventDto.from_flat_json(json_string)
            if pr_event is None:
                print("No PR event to process", flush = True)
                return
            self.__handle_pr_event(pr_event)
        except ValueError as e:
            print(f"Invalid JSON format: {e}", flush = True)
            return
        except Exception as e:
            print(f"Error processing pr_event: {e}", flush = True)
            return
    
    def __handle_pr_event(self, pr_event: PREventDto):
        if pr_event.pr_number not in self.graph.nodes:
            self.__handle_new_pr(pr_event)
        if pr_event.action == "opened":
                self.__handle_pr_opened_event(pr_event)
        elif pr_event.action == "submitted":
            if pr_event.review_state == "commented":
                self.__handle_pr_comment_event(pr_event)
            elif pr_event.review_state == "approved":
                self.__handle_pr_approved_event(pr_event)
        
    def __handle_pr_opened_event(self, pr_event: PREventDto):
        self.graph.add_edge(pr_event.pr_user, pr_event.pr_number, label="opened_pr")
        self.graph.add_edge(pr_event.pr_number, pr_event.repo_name, label="related_to_repo")
        for file in pr_event.pr_files_changed:
            self.graph.add_edge(pr_event.pr_number, file, label="modified_file")
            self.graph.add_edge(pr_event.repo_name, file, label="contains_file")

    def __handle_pr_comment_event(self, pr_event: PREventDto):
        self.graph.add_edge(pr_event.pr_user, pr_event.pr_number, label="commented_on_pr")

    def __handle_pr_approved_event(self, pr_event: PREventDto):
        self.graph.add_edge(pr_event.pr_user, pr_event.pr_number, label="approved_pr")

    def __handle_new_pr(self, pr_event: PREventDto):
        self.new_pr_event_publisher.publish(pr_event)

