import requests
import urllib.parse
from common.helpers.my_logger import MyLogger

logger = MyLogger().get_logger(__name__)

class GraphDataProvider:
    def __init__(self, base_url: str = "http://graph-service:8000"):
        logger.info("initialized with base URL: %s", base_url)
        self.base_url = base_url
    
    def get_pr_siblings_subgraph_by_common_modified_files(self, pr_number:int):
        url = f"{self.base_url}/subgraph/prs/{pr_number}/sibling-prs-by-common-files"
        response = requests.get(url, timeout=5)
        if response.status_code != 200:
            logger.debug("Unable to fetch PR siblings subgraph pr_number %d", pr_number)
            return[]
        logger.debug("Fetched PR siblings subgraph pr_number %d", pr_number)
        return response.json()