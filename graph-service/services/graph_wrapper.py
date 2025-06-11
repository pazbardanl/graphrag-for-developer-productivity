from  networkx import MultiDiGraph

class GraphWrapper:
    def __init__(self, graph:MultiDiGraph):
        self.graph = graph
    
    def add_opened_pr(self, pr_number: str, repo_name: str, pr_user: str, files_changed: list[any]):
        if not self.__node_exists(pr_number):
            self.graph.add_node(pr_number, type="pull_request")
        if not self.__node_exists(repo_name):
            self.graph.add_node(repo_name, type="repository")
        if not self.__node_exists(pr_user):
            self.graph.add_node(pr_user, type="user")

        self.__add_edge(pr_user, pr_number, label="opened_pr")
        self.__add_edge(pr_number, repo_name, label="related_to_repo")
        
        for file in files_changed:
            self.__add_edge(pr_number, file, label="modified_file")
            self.__add_edge(repo_name, file, label="contains_file")
    
    def add_comment_on_pr(self, pr_number: str, pr_user: any):
        if not self.__node_exists(pr_number):
            return
        if not self.__node_exists(pr_user):
            self.graph.add_node(pr_user, type="user")
        
        self.__add_edge(pr_user, pr_number, label="commented_on_pr")
    
    def add_approved_pr(self, pr_number: str, pr_user: any):
        if not self.__node_exists(pr_number):
            return
        if not self.__node_exists(pr_user):
            self.graph.add_node(pr_user, type="user")
        
        self.__add_edge(pr_user, pr_number, label="approved_pr")
        
    def get_all_nodes(self) -> list[any]:
        return list(self.graph.nodes)
    
    def get_all_edges(self) -> list[tuple[any, any]]:
        return list(self.graph.edges(data=True))

    def get_files_modified_by_pr(self, pr_number: str) -> list[any]:
        if not self.__node_exists(pr_number):
            return []
        files = [
            target
            for _, target, data in self.graph.out_edges(pr_number, data=True)
            if data.get("label") == "modified_file"
        ]
        return files
    
    def get_repo_related_to_pr(self, pr_number: str) -> list[any]:
        if not self.__node_exists(pr_number):
            return []
        repos = [
            target
            for _, target, data in self.graph.out_edges(pr_number, data=True)
            if data.get("label") == "related_to_repo"
        ]
        return repos
    
    def get_prs_modifying_file(self, file_name: str) -> list[any]:
        if not self.__node_exists(file_name):
            return []
        prs = [
            source
            for source, _, data in self.graph.in_edges(file_name, data=True)
            if data.get("label") == "modified_file"
        ]
        return prs

    def get_author_of_pr(self, pr_number: int) -> any:
        if not self.__node_exists(pr_number):
            return None
        for source, _, data in self.graph.in_edges(pr_number, data=True):
            if data.get("label") == "opened_pr":
                return source
        return None
    
    def get_approver_of_pr(self, pr_number: int) -> any:
        if not self.__node_exists(pr_number):
            return None
        for source, _, data in self.graph.in_edges(pr_number, data=True):
            if data.get("label") == "approved_pr":
                return source
        return None
    
    def get_commenters_of_pr(self, pr_number: int) -> list[any]:
        if not self.__node_exists(pr_number):
            return []
        commenters = [
            source
            for source, _, data in self.graph.in_edges(pr_number, data=True)
            if data.get("label") == "commented_on_pr"
        ]
        return commenters
    
    def __add_edge(self, source: any, target: any, label: str):
        if not self.__edge_exists(source, target, label):
            self.graph.add_edge(source, target, label=label)

    def __node_exists(self, node: any) -> bool:
        return node in self.graph.nodes

    def __edge_exists(self, source: any, target: any, label: str) -> bool:
        if not self.graph.has_edge(source, target):
            return False
        for key, edge_data in self.graph.get_edge_data(source, target).items():
            if edge_data.get("label") == label:
                return True
        return False