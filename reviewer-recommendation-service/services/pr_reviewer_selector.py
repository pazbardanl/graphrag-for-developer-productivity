from abc import ABC, abstractmethod
from common.models.pr_reviewer_recommendation_request import PrReviewerRecommendationRequest
from common.models.pr_reviewer_recommendation import PRReviewerRecommendation

class PRReviewerSelector(ABC):
    @abstractmethod
    def select(self, pr_reviewer_recommendation_request: PrReviewerRecommendationRequest) -> PRReviewerRecommendation:
        pass