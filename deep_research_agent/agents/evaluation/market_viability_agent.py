from strands import Agent
from typing import Optional
from deep_research_agent.agents.base_agent import BaseAgent
from deep_research_agent.common.schemas import EvaluationScore
from deep_research_agent.services.prompt_service import PromptService, AgentType
from deep_research_agent.utils.logger import logger


class MarketViabilityAgent(BaseAgent):
    def __init__(self, prompt_service: PromptService, agent: Optional[Agent] = None, model_id: Optional[str] = None):
        super().__init__(agent, model_id)
        self.prompt_service = prompt_service
        self._agent.system_prompt = self.prompt_service.get_system_prompt(AgentType.MARKET_VIABILITY)

    def execute(self, idea: str) -> EvaluationScore:
        """
        Scores the market viability and business potential of an idea.
        """
        logger.info(f"Executing Market Viability Agent for: {idea}")
        
        user_prompt = self.prompt_service.format_user_prompt(
            AgentType.MARKET_VIABILITY,
            "evaluate",
            idea=idea
        )
        
        score = self._agent.structured_output(EvaluationScore, user_prompt)
        score.agent = self.__class__.__name__
        return score
