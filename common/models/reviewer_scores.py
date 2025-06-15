
from pydantic import BaseModel

class ReviewerScoresDto(BaseModel):
    reviewer_user_id: str
    authored_score: float = 0.0
    commented_score: float = 0.0
    approved_score: float = 0.0
    
    def __add__(self, other):
        if not isinstance(other, ReviewerScoresDto):
            return NotImplemented
        return ReviewerScoresDto(
            reviewer_user_id=self.reviewer_user_id,
            authored_score=self.authored_score + other.authored_score,
            commented_score=self.commented_score + other.commented_score,
            approved_score=self.approved_score + other.approved_score
        )
    
    def __str__(self):
        return (
            f"ReviewerScoresDto(reviewer_user_id={self.reviewer_user_id}, "
            f"authored_score={self.authored_score}, "
            f"commented_score={self.commented_score}, "
            f"approved_score={self.approved_score})"
        )