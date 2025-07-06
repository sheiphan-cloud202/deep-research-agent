from typing import Any

from deep_research_agent.agents.base_agent import BaseAgent
from deep_research_agent.utils.logger import logger


class RankingAgent(BaseAgent):
    def __init__(self, *args, **kwargs):
        # This agent does not require prompt_service or a model, so we override __init__
        super().__init__()

    def execute(self, context: dict[str, Any]):
        """
        Ranks ideas based on their evaluation scores.
        """
        logger.info("Executing Ranking Agent...")
        scored_ideas = context["scored_ideas"]

        # Simple ranking logic: sum of scores
        ranked_ideas = sorted(
            scored_ideas.items(),
            key=lambda item: sum(score.score for score in item[1]),
            reverse=True,
        )

        context["ranked_ideas"] = ranked_ideas
        logger.info(f"Ranked Ideas:\n{ranked_ideas}\n")
