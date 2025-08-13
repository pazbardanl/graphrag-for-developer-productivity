import openai
import re
from services.pr_reviewer_selector import PRReviewerSelector
from common.helpers.graph_data_provider import GraphDataProvider
from common.models.pr_reviewer_recommendation import PRReviewerRecommendation
from common.models.selection_strategy import SelectionStrategy
from common.models.pr_reviewer_recommendation_request import PrReviewerRecommendationRequest
from common.helpers.my_logger import MyLogger

logger = MyLogger().get_logger(__name__)

class OpenAIPrReviewerSelector(PRReviewerSelector):
    MAX_TOKENS = 256
    TEMPERATURE = 0.2

    def __init__(self, graph_data_provider: GraphDataProvider):
        self.client = openai.OpenAI()
        self.graph_data_provider = graph_data_provider
        logger.info("initialized")

    def select(self, pr_reviewer_recommendation_request: PrReviewerRecommendationRequest) -> PRReviewerRecommendation:
        if not pr_reviewer_recommendation_request:
            logger.error(f"Empty (None) PR reviewer recommendation request, no recommendation (returning None).")
            return None
        if pr_reviewer_recommendation_request.selection_strategy != SelectionStrategy.OPENAI:
            logger.error(f"PR reviewer recommendation request routing error: selection strategy expected to be OPENAI, but is actually: ({pr_reviewer_recommendation_request.selection_strategy}), no recommendation (returning None).")
            return None
        if not pr_reviewer_recommendation_request.pr_number:
            logger.error(f"PR reviewer recommendation request does not contain a valid PR number ({pr_reviewer_recommendation_request.pr_number}), no recommendation (returning None).")
            return None
        pr_number = pr_reviewer_recommendation_request.pr_number
        pr_subgraph_json = self.graph_data_provider.get_pr_siblings_subgraph_by_common_modified_files(pr_number)
        logger.debug(f"PR-siblings subgraph json:{pr_subgraph_json}")
        if not pr_subgraph_json:
            logger.error(f"Empty PR-siblings subgraph for PR number {pr_number}, no recommendations (returning None).")
            return None
        prompt = self._get_prompt(pr_subgraph_json, pr_number)
        logger.debug(f"Generated prompt for OpenAI: {prompt}")
        ai_reply = self._get_open_ai_reply(prompt)
        recommendation  = self._build_recommendation(ai_reply, pr_reviewer_recommendation_request)
        if not recommendation:
            logger.debug(f"Cannot build recommendation from AI reply: {ai_reply}")
            return None
        logger.debug(f'PRReviewerRecommendation = {recommendation}')
        return recommendation
    
    def _get_prompt(self, pr_subgraph_json: str, pr_number: int) -> str:
        return (
            f"You are an expert in recommending code reviewers for pull requests.\n"
            f"You are given a subgraph in JSON format representing PRs and their relationships for a repository. "
            f"The subgraph includes the source PR (PR #{pr_number}), all PRs that share modified files with it, "
            f"and the authors, commenters, and approvers of these PRs, as well as the files they modified.\n"
            f"Your task is to analyze the subgraph and recommend the best reviewer for PR #{pr_number} using the following algorithm:\n"
            f"- For each PR that shares files with the source PR, calculate a weight based on the overlap of modified files: own_ratio = (number of overlapping files) / (number of files in this past PR), cross_ratio = (number of overlapping files) / (number of files in the current PR), and so overall_weight = own_ratio * cross_ratio.\n"
            f"- Level of Involvment: Weight your recommendations so that authoring and approving scores are most important (40% each), and commenting score is less important (20%).\n" 
            f"- Do not reflect or share the weight calculation method or the exact Level of Involvement weights in your reasoning, as they are internal.\n"
            f"- For each user, sum their scores for authored, approved, and commented PRs (weighted by PR files overlap as well as Level of Involvement).\n"
            f"- Do NOT recommend the author of the source PR.\n"
            f"- Do NOT elaborate on your calculations or the on the alogorithm, just recommend a reviewer and provide reasoning in general, no details.\n"
            f"- The user with the highest total score should be recommended as the reviewer.\n"
            f"Input subgraph:\n{pr_subgraph_json}\n"
            f"Please provide your response as follows:\n"
            f"<user_id>|<reasoning>\n"
            f"Where <user_id> is the recommended reviewer and <reasoning> is a brief explanation for your choice, referencing their involvement and the algorithm.\n"
            f"If for some reason you cannot conclude on a recommended reviewer, please stick to the format above by putting NO_RECOMMENDED_USER in <user_id>, and put the explanation for not reaching a conclusion in <reasoning>.\n"
            f"<user_id> should not contain anything other than recommended reviewer's name, if it exists. if not, then it be NO_RECOMMENDED_USER. DO NOT use <user_id> for any other purpose.\n"
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
    
    def _build_recommendation(self, ai_reply: str, pr_reviewer_recommendation_request: PrReviewerRecommendationRequest) -> PRReviewerRecommendation:
        try:
            recommended_reviewer, reasoning = ai_reply.split('|', 1)
            recommended_reviewer = self._clean_reviewer(recommended_reviewer)
            reasoning = reasoning.strip()
        except ValueError:
            logger.warning(f"Invalid response format from OpenAI: {ai_reply}, no recommendation generated. Returning None.")
            return None
        recommendation = PRReviewerRecommendation(
            pr_number=pr_reviewer_recommendation_request.pr_number,
            recommended_reviewer=recommended_reviewer,
            reasoning=reasoning,
            selection_strategy=pr_reviewer_recommendation_request.selection_strategy
        )
        return recommendation
    
    def _clean_reviewer(self, val):
        # Remove any leading/trailing whitespace and quotes
        return re.sub(r'^[\'"]+|[\'"]+$', '', val.strip())
