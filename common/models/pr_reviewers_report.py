from common.models.reviewer_scores import ReviewerScoresDto

class PRReviewerReport:
    def __init__(self, pr_number: int, reviewer_scores: list[ReviewerScoresDto]):
        self.pr_number = pr_number
        self.reviewer_scores = reviewer_scores