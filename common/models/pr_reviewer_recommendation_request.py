from pydantic import BaseModel, Field
from common.models.selection_strategy import SelectionStrategy

class PrReviewerRecommendationRequest(BaseModel):
    pr_number: int
    repo_name: str
    selection_strategy: SelectionStrategy