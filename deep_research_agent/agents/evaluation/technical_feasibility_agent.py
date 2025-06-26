from strands import Agent
from deep_research_agent.agents.base_agent import BaseAgent
from deep_research_agent.schemas import EvaluationScore


class TechnicalFeasibilityAgent(BaseAgent):
    def __init__(self, agent: Agent):
        super().__init__(agent)
        self._agent.system_prompt = (
            "You are a Technical Feasibility Agent. Your task is to evaluate a given idea and provide a score from 1-10 "
            "on its technical feasibility. You must also provide a justification for your score. "
            "Consider the required technologies, complexity, and potential challenges."
        )

    def execute(self, idea: str) -> EvaluationScore:
        """
        Scores the technical feasibility of an idea.
        """
        print(f"Executing Technical Feasibility Agent for: {idea}")
        
        score = self._agent.structured_output(
            EvaluationScore,
            f"Evaluate the technical feasibility of this idea: '{idea}'. "
            "Provide a score and a justification."
        )
        score.agent = self.__class__.__name__
        return score
