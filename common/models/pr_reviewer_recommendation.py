import json
from common.models.pr_reviewers_report import PRReviewerReport

class PRReviewerRecommendation:
    def __init__(self, pr_number: int, recommended_reviewer: str, reasoning: str):
        self.pr_number = pr_number
        self.recommended_reviewer = recommended_reviewer
        self.reasoning = reasoning

    def __str__(self):
        return (
            f"PRReviewerRecommendation(pr_number={self.pr_number}, "
            f"recommended_reviewer={self.recommended_reviewer}, "
            f"reasoning={self.reasoning})"
        )
    
    def model_dump_json(self):
        return json.dumps({
            "pr_number": self.pr_number,
            "recommended_reviewer": self.recommended_reviewer,
            "reasoning": self.reasoning
        })
