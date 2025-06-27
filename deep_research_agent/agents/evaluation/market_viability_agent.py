from strands import Agent
from typing import Optional
from deep_research_agent.agents.base_agent import BaseAgent
from deep_research_agent.schemas import EvaluationScore


class MarketViabilityAgent(BaseAgent):
    def __init__(self, agent: Optional[Agent] = None, model_id: Optional[str] = None):
        super().__init__(agent, model_id)
        self._agent.system_prompt = (
            "You are a Market Viability Agent. Your task is to evaluate a given idea and provide a score from 1-10 "
            "on its market viability and business potential. You must also provide a justification for your score. "
            "Consider the target user, market size, competition, and potential revenue streams."
        )

    def execute(self, idea: str) -> EvaluationScore:
        """
        Scores the market viability and business potential of an idea.
        """
        print(f"Executing Market Viability Agent for: {idea}")
        
        score = self._agent.structured_output(
            EvaluationScore,
            f"Evaluate the market viability of this idea: '{idea}'. "
            "Provide a score and a justification."
        )
        score.agent = self.__class__.__name__
        return score
