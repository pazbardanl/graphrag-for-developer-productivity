import requests
import urllib.parse
from common.helpers.my_logger import MyLogger
from common.models.selection_strategy import SelectionStrategy

logger = MyLogger().get_logger(__name__)

class UserDataProvider:
    def __init__(self, base_url: str = "http://user-data-service:8080"):
        logger.info("initialized with base URL: %s", base_url)
        self.base_url = base_url
    
    def get_repo_reviewer_selection_strategy(self, repo_name:str) -> SelectionStrategy:
        if not repo_name:
            logger.error("Repository name is empty or None")
            return SelectionStrategy.UNDETERMINED
        params = {'name': repo_name}
        query_string = urllib.parse.urlencode(params)
        url = f"{self.base_url}/repos/reviewer-selector-strategy?{query_string}"
        logger.debug("Request URL: %s", url)
        try:
            response = requests.get(url, timeout=5)
        except requests.exceptions.RequestException as e:
            logger.error("Error connecting to user-data-service for repo %s: %s", repo_name, e)
            return SelectionStrategy.UNDETERMINED
        if response.status_code != 200:
            logger.error("Unable to fetch reviewer selection strategy for repo %s: %s", repo_name, response.text)
            return[]
        logger.debug("Fetched reviewer selection strategy for repo %s : %s", repo_name, response.text)
        response_text = response.text.strip().lower()
        return SelectionStrategy.from_string(response_text)