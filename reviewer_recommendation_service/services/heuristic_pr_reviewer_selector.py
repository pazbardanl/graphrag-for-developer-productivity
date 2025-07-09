from .pr_reviewer_selector import PRReviewerSelector
from common.models.pr_event import PREventDto
from common.models.reviewer_scores import ReviewerScoresDto
from common.models.pr_reviewer_recommendation import PRReviewerRecommendation
from common.models.selection_strategy import SelectionStrategy
from common.helpers.graph_data_provider import GraphDataProvider
from common.helpers.my_logger import MyLogger

logger = MyLogger().get_logger(__name__)
AUTHORING_SCORE_WEIGHT = 0.4
APPROVING_SCORE_WEIGHT = 0.4
COMMENTING_SCORE_WEIGHT = 0.2

class HeuristicPRReviewerSelector(PRReviewerSelector):

    def __init__(self, graph_data_provider: GraphDataProvider):
        self.graph_data_provider = graph_data_provider
        logger.info("initialized")

    def select(self, pr_event: PREventDto) -> PRReviewerRecommendation:
        reviewer_scores_set = self._get_raw_reviewer_scores(pr_event)
        print(f"[D] reviewer_scores_set = {reviewer_scores_set}")
        selected_reviewer, selected_score = self._select_reviewer_by_max_weighted_score(reviewer_scores_set)
        reviewer_scores_set_sorted = sorted(reviewer_scores_set, key=lambda r: r.reviewer_user_id)
        return PRReviewerRecommendation(
            pr_number=pr_event.pr_number,
            recommended_reviewer=selected_reviewer,
            selection_strategy=SelectionStrategy.HEURISTIC,
            reasoning=f"Selected reviewer {selected_reviewer} with max weighted score of {selected_score}, based on heuristic scoring.",
            reviewers_scoring_array=reviewer_scores_set_sorted
        )

    def _get_raw_reviewer_scores(self, pr_event_dto: PREventDto) -> list[ReviewerScoresDto]:
        pr_weights = self._calculate_pr_weights_for_pr_event(pr_event_dto)
        print(f"[D] pr_weights = {pr_weights}")
        author = pr_event_dto.pr_user
        if not author:
            logger.error('PR author not provided')
            return {}
        reviewer_scores_set = self._calculate_reviewer_scores(pr_weights, author)
        return reviewer_scores_set
        
    def _calculate_pr_weights_for_pr_event(self, pr_event_dto: PREventDto) -> dict[int, float]:
        original_pr_number = pr_event_dto.pr_number
        repo_name = pr_event_dto.repo_name
        changed_files = pr_event_dto.pr_files_changed
        if not original_pr_number or not repo_name or not changed_files:
            logger.error('PR number, repo name or changed files not provided')
            return {}
        relevant_prs = self._get_relevant_prs(original_pr_number, repo_name, changed_files)
        pr_weights = self._calculate_pr_weights(relevant_prs, changed_files)
        return pr_weights
    
    def _get_relevant_prs(self, original_pr_number: int, repo_name: str, changed_files: list[str]) -> set[int]:
        relevant_prs = set()
        for file_name in changed_files:
            prs_modifying_file = self.graph_data_provider.get_prs_modifying_file(repo_name, file_name)
            relevant_prs.update(prs_modifying_file)
        relevant_prs.discard(original_pr_number)
        return relevant_prs

    def _calculate_pr_weights(self, relevant_prs: set[int], changed_files: list[str]) -> dict[int, float]:
        pr_weights = {}
        for pr_number in relevant_prs:
            if pr_number not in pr_weights:
                pr_weights[pr_number] = 0.0
            files_modified_by_pr = self.graph_data_provider.get_files_modified_by_pr(pr_number)
            if not files_modified_by_pr:
                continue
            overlapping_files = list(set(changed_files) & set(files_modified_by_pr))
            if overlapping_files:
                own_ratio = len(overlapping_files) / len(files_modified_by_pr)
                cross_ratio = len(overlapping_files) / len(changed_files)
                overall_ratio = own_ratio * cross_ratio
                pr_weights[pr_number] += overall_ratio
        return pr_weights
    
    def _calculate_reviewer_scores(self, pr_weights: dict[int, float], original_pr_author: str) -> list[ReviewerScoresDto]:
        pr_reviewer_scores: Dict[str, ReviewerScoresDto] = {}
        for pr_number, weight in pr_weights.items():
            author = self.graph_data_provider.get_pr_author(pr_number)
            approver = self.graph_data_provider.get_pr_approver(pr_number)
            commenters = self.graph_data_provider.get_pr_commenters(pr_number)
            if author:
                added_reviewer_score = ReviewerScoresDto(reviewer_user_id=author,authored_score = weight, approved_score=0.0, commented_score=0.0)
                pr_reviewer_scores[author] = pr_reviewer_scores.get(author, ReviewerScoresDto(reviewer_user_id=author)) + added_reviewer_score
            if approver:
                added_reviewer_score = ReviewerScoresDto(reviewer_user_id=approver,authored_score = 0.0, approved_score= weight, commented_score=0.0)
                pr_reviewer_scores[approver] = pr_reviewer_scores.get(approver, ReviewerScoresDto(reviewer_user_id=approver)) + added_reviewer_score
            for commenter in commenters:
                added_reviewer_score = ReviewerScoresDto(reviewer_user_id=commenter,authored_score = 0.0, approved_score= 0.0, commented_score= weight)
                pr_reviewer_scores[commenter] = pr_reviewer_scores.get(commenter, ReviewerScoresDto(reviewer_user_id=commenter)) + added_reviewer_score
        pr_reviewer_scores.pop(original_pr_author, None)
        return list(pr_reviewer_scores.values())
    
    def _select_reviewer_by_max_weighted_score(self, reviewer_scores: list[ReviewerScoresDto]) -> ReviewerScoresDto:
        user_to_weighted_score = {}
        if not reviewer_scores:
            return "NO_RECOMMENDED_USER", None
        for reviewer_score in reviewer_scores:
            user_to_weighted_score[reviewer_score.reviewer_user_id] = self._calculate_weighted_score(reviewer_score)
        print(f"[D] user_to_weighted_score = {user_to_weighted_score}")
        max_score = max(user_to_weighted_score.values())
        # Get all users with the max score
        max_users = [user for user, score in user_to_weighted_score.items() if score == max_score]
        # Choose the first alphabetically
        max_score_user = sorted(max_users)[0]
        return max_score_user, max_score

    def _calculate_weighted_score(self, reviewer_score: ReviewerScoresDto) -> float:
        return (AUTHORING_SCORE_WEIGHT * reviewer_score.authored_score +
                APPROVING_SCORE_WEIGHT * reviewer_score.approved_score +
                COMMENTING_SCORE_WEIGHT * reviewer_score.commented_score)