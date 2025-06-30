from strands import Agent
from typing import Optional
from deep_research_agent.agents.base_agent import BaseAgent
from deep_research_agent.schemas import EvaluationScore
from deep_research_agent.prompt_service import PromptService, AgentType


class MarketViabilityAgent(BaseAgent):
    def __init__(self, agent: Optional[Agent] = None, model_id: Optional[str] = None):
        super().__init__(agent, model_id)
        self._agent.system_prompt = PromptService.get_system_prompt(AgentType.MARKET_VIABILITY)

    def execute(self, idea: str) -> EvaluationScore:
        """
        Scores the market viability and business potential of an idea.
        """
        print(f"Executing Market Viability Agent for: {idea}")
        
        user_prompt = PromptService.format_user_prompt(
            AgentType.MARKET_VIABILITY,
            "evaluate",
            idea=idea
        )
        
        score = self._agent.structured_output(EvaluationScore, user_prompt)
        score.agent = self.__class__.__name__
        return score
