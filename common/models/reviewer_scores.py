class ReviewerScoresDto:
    def __init__(self, reviwer_user_id: str, authored_score: float, commented_score: float, approved_score: float):
        self.reviewer_user_id = reviwer_user_id
        self.authored_score = authored_score
        self.commented_score = commented_score
        self.approved_score = approved_score