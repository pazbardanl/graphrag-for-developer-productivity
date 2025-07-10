import requests
import urllib.parse
from common.helpers.my_logger import MyLogger
from common.models.selection_strategy import SelectionStrategy

logger = MyLogger().get_logger(__name__)

class UserDataProvider:
    def __init__(self, base_url: str = "http://user-data-service:8000"):
        logger.info("initialized with base URL: %s", base_url)
        self.base_url = base_url
    
    def get_repo_reviewer_selection_strategy(self, repo_name:str) -> SelectionStrategy:
        return SelectionStrategy.HEURISTIC