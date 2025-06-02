import networkx as nx
from common.models.pr_event import PREventDto

class Processor:
    def __init__(self):
        self.graph = nx.DiGraph()

    def process(self, json_string: str):
        try:
            pr_event = PREventDto.from_flat_json(json_string)
            if pr_event is None:
                print("No PR event to process", flush = True)
                return
            if pr_event.action == "opened":
                self.graph.add_edge(pr_event.pr_user, pr_event.pr_number, label="opened_pr")
                self.graph.add_edge(pr_event.pr_number, pr_event.repo_name, label="related_to_repo")
                for file in pr_event.pr_files_changed:
                    self.graph.add_edge(pr_event.pr_number, file, label="modified_file")
                    self.graph.add_edge(pr_event.repo_name, file, label="contains_file")
        except Exception as e:
            print(f"Error processing pr_event: {e}", flush = True)
            return
