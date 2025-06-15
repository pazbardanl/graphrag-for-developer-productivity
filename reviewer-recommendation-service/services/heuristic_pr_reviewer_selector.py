from services.pr_reviewer_selector import PRReviewerSelector
from common.models.pr_reviewer_recommendation import PRReviewerRecommendation
from common.models.pr_reviewers_report import PRReviewerReport
from common.helpers.my_logger import MyLogger

logger = MyLogger().get_logger(__name__)

class HeuristicPRReviewerSelector(PRReviewerSelector):
    def select(self, pr_report: PRReviewerReport) -> PRReviewerRecommendation:
        if not pr_report.reviewer_scores:
            logger.error(f"No reviewer candidates available for PR {pr_report.pr_number}, no recommentdation (returning None).")
            return None
        sorted_reviewers = sorted(pr_report.reviewer_scores, key=lambda x: x.authored_score, reverse=True)
        top_reviewer = sorted_reviewers[0]
        recommendation = PRReviewerRecommendation(
            pr_number=pr_report.pr_number,
            pr_reviewer_report=pr_report,
            recommended_reviewer=top_reviewer.reviewer_user_id,
            reasoning=f"Selected based on highest authored score: {top_reviewer.authored_score}"
        )
        logger.info(f'recommendation: {recommendation}')
        return recommendation