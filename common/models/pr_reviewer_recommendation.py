import json
from typing import Optional
from common.models.pr_reviewers_report import PRReviewerReport
from common.models.selection_strategy import SelectionStrategy
from common.models.reviewer_scores import ReviewerScoresDto

class PRReviewerRecommendation:
    def __init__(self, pr_number: int, recommended_reviewer: str, selection_strategy:SelectionStrategy, reasoning: str, reviewers_scoring_array: Optional[list[ReviewerScoresDto]] = None):
        self.pr_number = pr_number
        self.recommended_reviewer = recommended_reviewer
        self.selection_strategy = selection_strategy
        self.reasoning = reasoning
        self.reviewers_scoring_array = reviewers_scoring_array

    def __str__(self):
        base = (
            f"PRReviewerRecommendation(pr_number={self.pr_number}, "
            f"recommended_reviewer={self.recommended_reviewer}, "
            f"selection_strategy={self.selection_strategy}, "
            f"reasoning={self.reasoning}"
        )
        if self.reviewers_scoring_array is not None:
            base += f", reviewers_scoring_array={self.reviewers_scoring_array}"
        base += ")"
        return base
    
    def model_dump_json(self):
        data = {
            "pr_number": self.pr_number,
            "recommended_reviewer": self.recommended_reviewer,
            "selection_strategy": self.selection_strategy.value if hasattr(self.selection_strategy, "value") else self.selection_strategy,
            "reasoning": self.reasoning,
        }
        if self.reviewers_scoring_array is not None:
            data["reviewers_scoring_array"] = [scoring.model_dump_json() for scoring in self.reviewers_scoring_array]
        return json.dumps(data)
