from unittest.mock import MagicMock
from reviewer_recommendation_service.services.heuristic_pr_reviewer_selector import HeuristicPRReviewerSelector
from common.models.pr_event import PREventDto
from common.models.reviewer_scores import ReviewerScoresDto
from common.models.pr_reviewer_recommendation import PRReviewerRecommendation
from common.models.selection_strategy import SelectionStrategy
import pytest

@pytest.fixture
def selector_with_mocks():
    mock_graph_data_provider = MagicMock()
    mock_graph_data_provider.get_prs_modifying_file.side_effect = _mock_get_prs_modifying_file
    mock_graph_data_provider.get_files_modified_by_pr.side_effect = _mock_get_files_modified_by_pr
    mock_graph_data_provider.get_pr_author.side_effect = _mock_get_pr_author
    mock_graph_data_provider.get_pr_approver.side_effect = _mock_get_pr_approver
    mock_graph_data_provider.get_pr_commenters.side_effect = _mock_get_pr_commenters
    return HeuristicPRReviewerSelector(mock_graph_data_provider)

def _mock_get_prs_modifying_file(repo_name: str, file_name: str) -> list[int]:
    if repo_name == "repo1" and file_name == "file1":
        return [1]
    elif repo_name == "repo1" and file_name == "file2":
        return [1, 2]
    elif repo_name == "repo1" and file_name == "file3":
        return [1, 2]
    elif repo_name == "repo1" and file_name == "file4":
        return [4, 5]
    elif repo_name == "repo1" and file_name == "file5":
        return [4, 5]
    elif repo_name == "repo1" and file_name == "file6":
        return [5]
    elif repo_name == "repo1" and file_name == "file7":
        return [7, 8]
    elif repo_name == "repo1" and file_name == "file8":
        return [7, 8]
    elif repo_name == "repo1" and file_name == "file9":
        return [8, 9]
    elif repo_name == "repo1" and file_name == "file10":
        return [8, 9]
    elif repo_name == "repo1" and file_name == "file100":
        return [100]
    return []

def _mock_get_files_modified_by_pr(pr_number: int) -> list[str]:
    if pr_number == 1:
        return ["file1", "file2", "file3"]
    elif pr_number == 2:
        return ["file2", "file3"]
    elif pr_number == 4:
        return ["file4", "file5"]
    elif pr_number == 5:
        return ["file4", "file5",  "file6"]
    elif pr_number == 7:
        return ["file7", "file8"]
    elif pr_number == 8:
        return ["file7", "file8", "file9", "file10"]
    elif pr_number == 9:
        return ["file9", "file10"]
    elif pr_number == 100:
        return ["file100", "file101"]
    return []

def _mock_get_pr_author(pr_number: int) -> str:
    if pr_number == 1:
        return "user1"
    elif pr_number == 2:
        return "user2"
    elif pr_number == 4:
        return "user4"
    elif pr_number == 5:
        return "user4"
    elif pr_number == 7:
        return "user7"
    elif pr_number == 8:
        return "user8"
    elif pr_number == 9:
        return "user9"
    elif pr_number == 100:
        return "user100"
    return "unknown"

def _mock_get_pr_approver(pr_number: int) -> str:
    if pr_number == 1:
        return "user2"
    elif pr_number == 2:
        return "user1"
    elif pr_number == 4:
        return None
    elif pr_number == 5:
        return None
    elif pr_number == 7:
        return "user9"
    elif pr_number == 8:
        return None
    elif pr_number == 9:
        return "user7"
    elif pr_number == 100:
        return None
    return None

def _mock_get_pr_commenters(pr_number: int) -> list[str]:
    if pr_number == 1:
        return ["user2","user3"]
    elif pr_number == 2:
        return ["user1", "user3"]
    elif pr_number == 4:
        return []
    elif pr_number == 5:
        return []
    elif pr_number == 7:
        return ["user9"]
    elif pr_number == 8:
        return []
    elif pr_number == 9:
        return ["user7"]
    elif pr_number == 100:
        return []
    return []

@pytest.fixture
def pr1_pr_event_dto():
    return PREventDto(
        action="opened",
        sender="user1",
        pr_number=1,
        repo_name="repo1",
        pr_user="user1",
        pr_files_changed=["file1", "file2", "file3"]
    )

@pytest.fixture
def pr100_pr_event_dto():
    return PREventDto(
        action="opened",
        sender="user100",
        pr_number=100,
        repo_name="repo1",
        pr_user="user100",
        pr_files_changed=["file100", "file101"]
    )

@pytest.fixture
def pr100_pr_event_dto_no_changed_files():
    return PREventDto(
        action="opened",
        sender="user100",
        pr_number=100,
        repo_name="repo1",
        pr_user="user100",
        pr_files_changed=[]
    )

@pytest.fixture
def pr4_pr_event_dto():
    return PREventDto(
        action="opened",
        sender="user4",
        pr_number=4,
        repo_name="repo1",
        pr_user="user4",
        pr_files_changed=["file4", "file5"]
    )

@pytest.fixture
def pr8_pr_event_dto():
    return PREventDto(
        action="opened",
        sender="user8",
        pr_number=8,
        repo_name="repo1",
        pr_user="user8",
        pr_files_changed=["file7", "file8", "file9", "file10"]
    )

def test_heuristic_pr_reviewer_selector_sanity(selector_with_mocks, pr1_pr_event_dto):
    expected_pr_reviewer_recommendation = PRReviewerRecommendation(
        pr_number=1,
        recommended_reviewer="user2",
        selection_strategy=SelectionStrategy.HEURISTIC,
        reasoning="Selected reviewer user2 with max weighted score of 0.26666666666666666, based on heuristic scoring.",
        reviewers_scoring_array=[
            ReviewerScoresDto(reviewer_user_id="user2", authored_score=0.6666666666666666, approved_score=0.0, commented_score=0.0),
            ReviewerScoresDto(reviewer_user_id="user3", authored_score=0.0, approved_score=0.0, commented_score=0.6666666666666666)
        ]
    )
    actual_pr_reviewer_recommendation = selector_with_mocks.select(pr1_pr_event_dto)
    print(f"EXPECTED: {expected_pr_reviewer_recommendation}")
    print(f"ACTUAL: {actual_pr_reviewer_recommendation}")
    assert actual_pr_reviewer_recommendation == expected_pr_reviewer_recommendation

def test_heuristic_pr_reviewer_selector_no_changed_files(selector_with_mocks, pr100_pr_event_dto_no_changed_files):
    expected_pr_reviewer_recommendation = PRReviewerRecommendation(
        pr_number=100,
        recommended_reviewer="NO_RECOMMENDED_USER",
        selection_strategy=SelectionStrategy.HEURISTIC,
        reasoning="Selected reviewer NO_RECOMMENDED_USER with max weighted score of None, based on heuristic scoring.",
        reviewers_scoring_array=[]
    )
    actual_pr_reviewer_recommendation = selector_with_mocks.select(pr100_pr_event_dto_no_changed_files)
    print(f"EXPECTED: {expected_pr_reviewer_recommendation}")
    print(f"ACTUAL: {actual_pr_reviewer_recommendation}")
    assert actual_pr_reviewer_recommendation == expected_pr_reviewer_recommendation

def test_heuristic_pr_reviewer_selector_exclude_author(selector_with_mocks, pr4_pr_event_dto):
    expected_pr_reviewer_recommendation = PRReviewerRecommendation(
        pr_number=4,
        recommended_reviewer="NO_RECOMMENDED_USER",
        selection_strategy=SelectionStrategy.HEURISTIC,
        reasoning="Selected reviewer NO_RECOMMENDED_USER with max weighted score of None, based on heuristic scoring.",
        reviewers_scoring_array=[]
    )
    actual_pr_reviewer_recommendation = selector_with_mocks.select(pr4_pr_event_dto)
    print(f"EXPECTED: {expected_pr_reviewer_recommendation}")
    print(f"ACTUAL: {actual_pr_reviewer_recommendation}")
    assert actual_pr_reviewer_recommendation == expected_pr_reviewer_recommendation

def test_heuristic_pr_reviewer_selector_no_relevant_prs(selector_with_mocks, pr100_pr_event_dto):
    expected_pr_reviewer_recommendation = PRReviewerRecommendation(
        pr_number=100,
        recommended_reviewer="NO_RECOMMENDED_USER",
        selection_strategy=SelectionStrategy.HEURISTIC,
        reasoning="Selected reviewer NO_RECOMMENDED_USER with max weighted score of None, based on heuristic scoring.",
        reviewers_scoring_array=[]
    )
    actual_pr_reviewer_recommendation = selector_with_mocks.select(pr100_pr_event_dto)
    print(f"EXPECTED: {expected_pr_reviewer_recommendation}")
    print(f"ACTUAL: {actual_pr_reviewer_recommendation}")
    assert actual_pr_reviewer_recommendation == expected_pr_reviewer_recommendation

def test_heuristic_pr_reviewer_selector_tie(selector_with_mocks, pr8_pr_event_dto):
    expected_pr_reviewer_recommendation = PRReviewerRecommendation(
        pr_number=8,
        recommended_reviewer="user7",
        selection_strategy=SelectionStrategy.HEURISTIC,
        reasoning="Selected reviewer user7 with max weighted score of 0.5, based on heuristic scoring.",
        reviewers_scoring_array=[
            ReviewerScoresDto(reviewer_user_id="user7", authored_score=0.5, approved_score=0.5, commented_score=0.5),
            ReviewerScoresDto(reviewer_user_id="user9", authored_score=0.5, approved_score=0.5, commented_score=0.5)
        ]
    )
    actual_pr_reviewer_recommendation = selector_with_mocks.select(pr8_pr_event_dto)
    print(f"EXPECTED: {expected_pr_reviewer_recommendation}")
    print(f"ACTUAL: {actual_pr_reviewer_recommendation}")
    assert actual_pr_reviewer_recommendation == expected_pr_reviewer_recommendation

