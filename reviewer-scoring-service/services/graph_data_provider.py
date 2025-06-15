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
            return[]
        return response.json()
    
    def get_files_modified_by_pr(self, pr_number: int) -> list[str]:
        url = f"{self.base_url}/prs/{pr_number}/files"
        response = requests.get(url, timeout=5)
        if response.status_code != 200:
            return []
        return response.json()
    
    def get_pr_author(self, pr_number: int) -> str:
        url = f"{self.base_url}/prs/{pr_number}/author"
        response = requests.get(url, timeout=5)
        if response.status_code != 200:
            return None
        return response.json()
    
    def get_pr_approver(self, pr_number: int) -> str:
        url = f"{self.base_url}/prs/{pr_number}/approver"
        response = requests.get(url, timeout=5)
        if response.status_code != 200:
            return None
        return response.json()
    
    def get_pr_commenters(self, pr_number: int) -> list[str]:
        url = f"{self.base_url}/prs/{pr_number}/commenters"
        response = requests.get(url, timeout=5)
        if response.status_code != 200:
            return []
        return response.json()