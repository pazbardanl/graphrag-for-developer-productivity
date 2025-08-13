import requests
import urllib.parse
from common.helpers.my_logger import MyLogger

logger = MyLogger().get_logger(__name__)

class GraphDataProvider:
    def __init__(self, base_url: str = "http://graph-service:8000"):
        logger.info("initialized with base URL: %s", base_url)
        self.base_url = base_url

    def get_prs_modifying_file(self, repo_name: str, file_name: str) -> list[int]:
        repo_encoded = urllib.parse.quote(repo_name, safe='')
        file_encoded = urllib.parse.quote(file_name, safe='')
        url = f"{self.base_url}/repos/{repo_encoded}/files/{file_encoded}/prs"
        response = requests.get(url, timeout=5)
        if response.status_code != 200:
            logger.debug("Unable to fetch PRs modifying file %s in repo %s: %s", file_name, repo_name, response.text)
            return[]
        logger.debug("Fetched PRs modifying file %s in repo %s: %s", file_name, repo_name, response.json())
        return response.json()
    
    def get_files_modified_by_pr(self, pr_number: int) -> list[str]:
        url = f"{self.base_url}/prs/{pr_number}/files"
        response = requests.get(url, timeout=5)
        if response.status_code != 200:
            logger.debug("Unable to fetch files modified by PR %d: %s", pr_number, response.text)
            return []
        logger.debug("Fetched files modified by PR %d: %s", pr_number, response.json())
        return response.json()
    
    def get_pr_author(self, pr_number: int) -> str:
        url = f"{self.base_url}/prs/{pr_number}/author"
        response = requests.get(url, timeout=5)
        if response.status_code != 200:
            logger.debug("Unable to fetch author for PR %d: %s", pr_number, response.text)
            return None
        logger.debug("Fetched author for PR %d: %s", pr_number, response.json())
        return response.json()
    
    def get_pr_approver(self, pr_number: int) -> str:
        url = f"{self.base_url}/prs/{pr_number}/approver"
        response = requests.get(url, timeout=5)
        if response.status_code != 200:
            logger.debug("Unable to fetch approver for PR %d: %s", pr_number, response.text)
            return None
        logger.debug("Fetched approver for PR %d: %s", pr_number, response.json())
        return response.json()
    
    def get_pr_commenters(self, pr_number: int) -> list[str]:
        url = f"{self.base_url}/prs/{pr_number}/commenters"
        response = requests.get(url, timeout=5)
        if response.status_code != 200:
            logger.debug("Unable to fetch commenters for PR %d: %s", pr_number, response.text)
            return []
        logger.debug("Fetched commenters for PR %d: %s", pr_number, response.json())
        return response.json()
    
    def get_pr_siblings_subgraph_by_common_modified_files(self, pr_number:int):
        url = f"{self.base_url}/subgraph/prs/{pr_number}/sibling-prs-by-common-files"
        response = requests.get(url, timeout=5)
        if response.status_code != 200:
            logger.debug("Unable to fetch PR siblings subgraph pr_number %d", pr_number)
            return[]
        logger.debug("Fetched PR siblings subgraph pr_number %d", pr_number)
        return response.json()