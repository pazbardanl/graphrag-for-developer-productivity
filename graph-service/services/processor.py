from common.models.pr_event import PREventDto
from services.publisher import Publisher
from services.graph_wrapper import GraphWrapper
from common.helpers.my_logger import MyLogger

logger = MyLogger().get_logger(__name__)

class Processor:
    def __init__(self, graph_wrapper: GraphWrapper, new_pr_event_publisher: Publisher):
        logger.info("initialized")
        self.graph_wrapper = graph_wrapper
        self.new_pr_event_publisher = new_pr_event_publisher
    
    def process(self, json_string: str):
        try:
            pr_event = PREventDto.from_flat_json(json_string)
            if pr_event is None:
                logger.error("No PR event to process")
                return
            self.__handle_pr_event(pr_event)
        except ValueError as e:
            logger.error(f"Invalid JSON format: {e}")
            return
        except Exception as e:
            logger.error(f"Error processing pr_event: {e}")
            return
    
    def __handle_pr_event(self, pr_event: PREventDto):
        if pr_event.pr_number not in self.graph_wrapper.get_all_nodes():
            self.__handle_new_pr(pr_event)
        if pr_event.action == "opened":
                self.__handle_pr_opened_event(pr_event)
        elif pr_event.action == "submitted":
            if pr_event.review_state == "commented":
                self.__handle_pr_comment_event(pr_event)
            elif pr_event.review_state == "approved":
                self.__handle_pr_approved_event(pr_event)
        
    def __handle_pr_opened_event(self, pr_event: PREventDto):
        self.graph_wrapper.add_opened_pr(pr_event.pr_number, pr_event.repo_name, pr_event.pr_user, pr_event.pr_files_changed)

    def __handle_pr_comment_event(self, pr_event: PREventDto):
        self.graph_wrapper.add_comment_on_pr(pr_event.pr_number, pr_event.pr_user)

    def __handle_pr_approved_event(self, pr_event: PREventDto):
        self.graph_wrapper.add_approved_pr(pr_event.pr_number, pr_event.pr_user)

    def __handle_new_pr(self, pr_event: PREventDto):
        self.new_pr_event_publisher.publish(pr_event)

