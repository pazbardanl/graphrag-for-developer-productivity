
from graph_service.services.graph_wrapper import GraphWrapper
from networkx import MultiDiGraph

def test_get_pr_siblings_subgraph_by_common_modified_files__sanity():
    # Create a sample graph
    graph = MultiDiGraph()
    wrapper = GraphWrapper(graph)
    # Add nodes and edges to the graph
    wrapper.add_opened_pr("PR1", "repo1", "user1", ["file1", "file2"])
    wrapper.add_opened_pr("PR2", "repo1", "user2", ["file2", "file3"])
    wrapper.add_opened_pr("PR3", "repo1", "user3", ["file3"])
    # Get the subgraph for PR1
    subgraph = wrapper.get_pr_siblings_subgraph_by_common_modified_files("PR1")
    # Check if the subgraph contains the expected nodes and edges
    result_nodes = set(subgraph.nodes)
    assert len(result_nodes) == 7  # user1, user2, PR1, PR2, file1, file2, file3
    assert len(subgraph.edges) == 6  # user1>PR1, user2>PR2, PR1>file1, PR1>file2, PR2>file2, PR2>file3
    assert "PR1" in result_nodes
    assert "PR2" in result_nodes
    assert "user1" in result_nodes
    assert "user2" in result_nodes
    assert "file1" in result_nodes
    assert "file2" in result_nodes
    assert "file3" in result_nodes
    assert subgraph.has_edge("user1", "PR1")
    assert subgraph.has_edge("user2", "PR2")
    assert subgraph.has_edge("PR1", "file1")
    assert subgraph.has_edge("PR1", "file2")
    assert subgraph.has_edge("PR2", "file2")
    assert subgraph.has_edge("PR2", "file3")

def test_get_pr_siblings_subgraph_by_common_modified_files__no_common_files():
    # Create a sample graph
    graph = MultiDiGraph()
    wrapper = GraphWrapper(graph)
    # Add nodes and edges to the graph
    wrapper.add_opened_pr("PR1", "repo1", "user1", ["file1"])
    wrapper.add_opened_pr("PR2", "repo1", "user2", ["file2"])
    # Get the subgraph for PR1
    subgraph = wrapper.get_pr_siblings_subgraph_by_common_modified_files("PR1")
    # Check that subrgraph contains only the PR and its user
    result_nodes = set(subgraph.nodes)
    assert len(result_nodes) == 3
    assert len(subgraph.edges) == 2
    assert "user1" in result_nodes
    assert "PR1" in result_nodes
    assert "file1" in result_nodes
    assert subgraph.has_edge("user1", "PR1")
    assert subgraph.has_edge("PR1", "file1")

def test_get_pr_siblings_subgraph_by_common_modified_files__no_pr():
    # Create a sample graph
    graph = MultiDiGraph()
    wrapper = GraphWrapper(graph)
    # Get the subgraph for a non-existing PR
    subgraph = wrapper.get_pr_siblings_subgraph_by_common_modified_files("PR1")
    # Check that the subgraph is empty
    assert len(subgraph.nodes) == 0
    assert len(subgraph.edges) == 0

def test_get_pr_siblings_subgraph_by_common_modified_files__multiple_siblings():
    # Create a sample graph
    graph = MultiDiGraph()
    wrapper = GraphWrapper(graph)
    # Add nodes and edges to the graph
    wrapper.add_opened_pr("PR1", "repo1", "user1", ["file1", "file2", "file3"])
    wrapper.add_opened_pr("PR2", "repo1", "user2", ["file2", "file3"])
    wrapper.add_opened_pr("PR3", "repo1", "user3", ["file3"])
    wrapper.add_opened_pr("PR4", "repo1", "user4", ["file4"])
    wrapper.add_opened_pr("PR5", "repo1", "user5", ["file5"])
    # Get the subgraph for PR1
    subgraph = wrapper.get_pr_siblings_subgraph_by_common_modified_files("PR1")
    # Check if the subgraph contains the expected nodes and edges
    result_nodes = set(subgraph.nodes)
    assert len(result_nodes) == 9  # user1, user2, user3, PR1, PR2, PR3, file1, file2, file3
    assert len(subgraph.edges) == 9  # user1>PR1, user2>PR2, user3>PR3, PR1>file1, PR1>file2, PR1>file3, PR2>file2, PR2>file3, PR3>file3
    assert "PR1" in result_nodes
    assert "PR2" in result_nodes
    assert "PR3" in result_nodes
    assert "user1" in result_nodes
    assert "user2" in result_nodes
    assert "user3" in result_nodes
    assert "file1" in result_nodes
    assert "file2" in result_nodes
    assert "file3" in result_nodes
    assert subgraph.has_edge("user1", "PR1")
    assert subgraph.has_edge("user2", "PR2")
    assert subgraph.has_edge("user3", "PR3")
    assert subgraph.has_edge("PR1", "file1")
    assert subgraph.has_edge("PR1", "file2")
    assert subgraph.has_edge("PR1", "file3")
    assert subgraph.has_edge("PR2", "file2")
    assert subgraph.has_edge("PR2", "file3")
    assert subgraph.has_edge("PR3", "file3")

def test_get_pr_siblings_subgraph_by_common_modified_files__with_approvers_and_commenters():
    graph = MultiDiGraph()
    wrapper = GraphWrapper(graph)
    # Add PRs with authors
    wrapper.add_opened_pr("PR1", "repo1", "author1", ["file1", "file2"])
    wrapper.add_opened_pr("PR2", "repo1", "author2", ["file2", "file3"])
    # Add approvers
    wrapper.add_approved_pr("PR1", "approver1")
    wrapper.add_approved_pr("PR2", "approver2")
    # Add commenters
    wrapper.add_comment_on_pr("PR1", "commenter1")
    wrapper.add_comment_on_pr("PR1", "commenter2")
    wrapper.add_comment_on_pr("PR2", "commenter3")
    # Get the subgraph for PR1
    subgraph = wrapper.get_pr_siblings_subgraph_by_common_modified_files("PR1")
    result_nodes = set(subgraph.nodes)
    assert len(result_nodes) == 12
    assert len(subgraph.edges) == 11
    assert "author1" in result_nodes
    assert "author2" in result_nodes
    assert "approver1" in result_nodes
    assert "approver2" in result_nodes
    assert "commenter1" in result_nodes
    assert "commenter2" in result_nodes
    assert "commenter3" in result_nodes
    assert "PR1" in result_nodes
    assert "PR2" in result_nodes
    assert "file1" in result_nodes
    assert "file2" in result_nodes
    assert "file3" in result_nodes
    assert subgraph.has_edge("author1", "PR1")
    assert subgraph.has_edge("author2", "PR2")
    assert subgraph.has_edge("approver1", "PR1")
    assert subgraph.has_edge("approver2", "PR2")
    assert subgraph.has_edge("commenter1", "PR1")
    assert subgraph.has_edge("commenter2", "PR1")
    assert subgraph.has_edge("commenter3", "PR2")
    assert subgraph.has_edge("PR1", "file1")
    assert subgraph.has_edge("PR1", "file2")
    assert subgraph.has_edge("PR2", "file2")
    assert subgraph.has_edge("PR2", "file3")