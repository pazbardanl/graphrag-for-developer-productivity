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
        return SelectionStrategy.OPENAI
        # url = f"{self.base_url}/subgraph/prs/{pr_number}/sibling-prs-by-common-files"
        # response = requests.get(url, timeout=5)
        # if response.status_code != 200:
        #     logger.debug("Unable to fetch PR siblings subgraph pr_number %d", pr_number)
        #     return[]
        # logger.debug("Fetched PR siblings subgraph pr_number %d", pr_number)
        # return response.json()