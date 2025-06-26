from strands import Agent
from deep_research_agent.agents.base_agent import BaseAgent
from deep_research_agent.schemas import EvaluationScore


class EthicalGuardianAgent(BaseAgent):
    def __init__(self, agent: Agent):
        super().__init__(agent)
        self._agent.system_prompt = (
            "You are an Ethical Guardian Agent. Your task is to evaluate a given idea and provide a score from 1-10 "
            "on its ethical implications. You must also provide a justification for your score. "
            "Consider safety, fairness, bias, privacy, and potential for misuse."
        )

    def execute(self, idea: str) -> EvaluationScore:
        """
        Scores an idea for safety, fairness, and bias.
        """
        print(f"Executing Ethical Guardian Agent for: {idea}")
        
        score = self._agent.structured_output(
            EvaluationScore,
            f"Evaluate the ethical implications of this idea: '{idea}'. "
            "Provide a score and a justification."
        )
        score.agent = self.__class__.__name__
        return score
