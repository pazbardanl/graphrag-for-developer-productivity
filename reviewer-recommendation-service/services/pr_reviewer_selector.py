from abc import ABC, abstractmethod
from common.models.pr_reviewers_report import PRReviewerReport
from common.models.pr_reviewer_recommendation import PRReviewerRecommendation

class PRReviewerSelector(ABC):
    @abstractmethod
    def select(self, pr_report: PRReviewerReport) -> PRReviewerRecommendation:
        pass