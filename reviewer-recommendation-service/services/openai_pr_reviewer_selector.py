import openai
import re
from services.pr_reviewer_selector import PRReviewerSelector
from common.models.pr_reviewer_recommendation import PRReviewerRecommendation
from common.models.pr_reviewers_report import PRReviewerReport
from common.helpers.my_logger import MyLogger

logger = MyLogger().get_logger(__name__)

class OpenAIPrReviewerSelector(PRReviewerSelector):
    MAX_TOKENS = 256
    TEMPERATURE = 0.2

    def __init__(self):
        self.client = openai.OpenAI()
        logger.info("initialized")

    def select(self, pr_report: PRReviewerReport) -> PRReviewerRecommendation:
        if not pr_report.reviewer_scores:
            logger.error(f"No reviewer candidates available for PR {pr_report.pr_number}, no recommendations (returning None).")
            return None
        prompt = self._get_prompt(pr_report)
        logger.debug(f"Generated prompt for OpenAI: {prompt}")
        ai_reply = self._get_open_ai_reply(prompt)
        logger.debug(f"OpenAI reply received: {ai_reply}")
        recommendation  = self._build_recommendation(ai_reply, pr_report)
        if not recommendation:
            logger.debug(f"Cannot build recommendation from AI reply: {ai_reply}")
            return None
        logger.debug(f'PRReviewerRecommendation = {recommendation}')
        logger.info(f"PR number : {recommendation.pr_number}, Recommended reviewer: {recommendation.recommended_reviewer}") 
        return recommendation
    
    def _get_prompt(self, pr_report: PRReviewerReport) -> str:
        return (
            f"Select a reviewer for PR #{pr_report.pr_number} based on the following scores:\n"
            f"{pr_report.model_dump_json()}. \n"
            f"Keep in mind these scores are given based on a user's involvement with reviewing, approving and commenting on specific files related to the given PR, and not just general PR engagement scores.\n"
            f"Please select the most suitable reviewer based on their authored score, review count, and file involvement.\n"
            f"Provide the user ID of the recommended reviewer and a brief reasoning for your choice.\n"
            f"also: weight your recommendations so that authored_score and approved_score scores are most important (40% each), and commented_score is less important (20%). Do not reflect or share these exact weights in your reasoning, as they are internal.\n"
            "Please structure your response with the user ID of the recommended reviewer first, and then the reasoning behind your choice, with a pipe (|) separating them.\n"
        )

    def _get_open_ai_reply(self, prompt: str) -> str:
        logger.debug(f"Sending prompt to OpenAI: {prompt}")
        response = self.client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an expert in selecting the best reviewers for pull requests."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=self.MAX_TOKENS,
            temperature=self.TEMPERATURE
        )
        ai_reply = response.choices[0].message.content.strip()
        self._validate_ai_reply(ai_reply)
        logger.debug(f"OpenAI response: {ai_reply}")
        return ai_reply
    
    def _validate_ai_reply(self, ai_reply: str):
        if not ai_reply:
            logger.error("OpenAI response is empty")
            raise ValueError("OpenAI response is empty")
    
    def _build_recommendation(self, ai_reply: str, pr_report: PRReviewerReport) -> PRReviewerRecommendation:
        try:
            recommended_reviewer, reasoning = ai_reply.split('|', 1)
            recommended_reviewer = self.clean_reviewer(recommended_reviewer)
            reasoning = reasoning.strip()
        except ValueError:
            logger.error(f"Invalid response format from OpenAI: {ai_reply}")
            raise ValueError("Invalid response format from OpenAI.")
        recommendation = PRReviewerRecommendation(
            pr_number=pr_report.pr_number,
            pr_reviewer_report=pr_report,
            recommended_reviewer=recommended_reviewer,
            reasoning=reasoning
        )
        return recommendation
    
    def clean_reviewer(self, val):
        # Remove any leading/trailing whitespace and quotes
        return re.sub(r'^[\'"]+|[\'"]+$', '', val.strip())
