import json
from pydantic import BaseModel
from typing import List
from common.models.reviewer_scores import ReviewerScoresDto

class PRReviewerReport(BaseModel):
    pr_number: int
    reviewer_scores: List[ReviewerScoresDto]
    
    def __str__(self):
        return (
            f"PRReviewerReport(pr_number={self.pr_number}, "
            f"reviewer_scores=[{', '.join(str(score) for score in self.reviewer_scores)}])"
        )