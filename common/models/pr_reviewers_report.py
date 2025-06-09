import json
from common.models.reviewer_scores import ReviewerScoresDto

class PRReviewerReport:
    def __init__(self, pr_number: int, reviewer_scores: list[ReviewerScoresDto]):
        self.pr_number = pr_number
        self.reviewer_scores = reviewer_scores
    
    def __str__(self):
        return (
            f"PRReviewerReport(pr_number={self.pr_number}, "
            f"reviewer_scores=[{', '.join(str(score) for score in self.reviewer_scores)}])"
        )

    def model_dump_json(self):
        return json.dumps({
            "pr_number": self.pr_number,
            "reviewer_scores": [
                {
                    "reviewer_user_id": score.reviewer_user_id,
                    "authored_score": score.authored_score,
                    "commented_score": score.commented_score,
                    "approved_score": score.approved_score,
                }
                for score in self.reviewer_scores
            ]
        })