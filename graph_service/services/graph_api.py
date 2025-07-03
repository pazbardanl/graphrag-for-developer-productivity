import networkx as nx
from fastapi import FastAPI, HTTPException
from services.graph_wrapper import GraphWrapper
from common.helpers.my_logger import MyLogger

logger = MyLogger().get_logger(__name__)

class GraphAPI:
    def __init__(self, graph_wrapper: GraphWrapper):
        self.app = FastAPI()
        self.graph_wrapper = graph_wrapper
        self.__setup_routes()

    def __setup_routes(self):
        @self.app.get("/nodes")
        def get_nodes():
            return list(self.graph_wrapper.get_all_nodes())
        
        @self.app.get("/edges")
        def get_edges():
            return list(self.graph_wrapper.get_all_edges())

        @self.app.get("/prs/{pr_id}/files")
        def get_files_for_pr(pr_id: int):
            result = self.graph_wrapper.get_files_modified_by_pr(pr_id)
            if not result:
                logger.warning(f"PR {pr_id} not found or does not modify any files")
                raise HTTPException(status_code=404, detail="PR not found or does not modify any files")
            return result
        
        @self.app.get("/prs/{pr_id}/repos")
        def get_repos_for_pr(pr_id: int):
            result = self.graph_wrapper.get_repo_related_to_pr(pr_id)
            if not result:
                logger.warning(f"PR {pr_id} not found or does not relate to any repositories")
                raise HTTPException(status_code=404, detail="PR not found or does not relate to any repositories")
            return result

        @self.app.get("/repos/{repo_name:path}/files/{file_name:path}/prs")
        def get_prs_modifying_file(repo_name: str, file_name: str):
            result = self.graph_wrapper.get_prs_modifying_file(file_name)
            if not result:
                logger.debug(f"File {file_name} in repo {repo_name} not found or does not have any modifying PRs")
                raise HTTPException(status_code=404, detail=f"File {file_name} in repo {repo_name} not found or does not have any modifying PRs")
            return result

        @self.app.get("/prs/{pr_id}/author")
        def get_author_of_pr(pr_id: int):
            result = self.graph_wrapper.get_author_of_pr(pr_id)
            if result is None:
                logger.warning(f"PR {pr_id} not found or has no author")
                raise HTTPException(status_code=404, detail="PR not found or has no author")
            return result

        @self.app.get("/prs/{pr_id}/approver")
        def get_approver_of_pr(pr_id: int):
            result = self.graph_wrapper.get_approver_of_pr(pr_id)
            if result is None:
                logger.debug(f"PR {pr_id} not found or has no approver")
                raise HTTPException(status_code=404, detail="PR not found or has no approver")
            return result

        @self.app.get("/prs/{pr_id}/commenters")
        def get_commenters_of_pr(pr_id: int):
            result = self.graph_wrapper.get_commenters_of_pr(pr_id)
            if not result:
                logger.debug(f"PR {pr_id} not found or has no commenters")
                raise HTTPException(status_code=404, detail="PR not found or has no commenters")
            return result
