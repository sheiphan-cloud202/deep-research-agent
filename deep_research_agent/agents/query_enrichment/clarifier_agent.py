from strands import Agent
from deep_research_agent.agents.base_agent import BaseAgent


class ClarifierAgent(BaseAgent):
    def __init__(self, agent: Agent):
        super().__init__(agent)
        self._agent.system_prompt = (
            "You are a Clarifier Agent. Your job is to analyze a user's prompt "
            "and ask 2-3 specific, targeted questions to help refine their idea. "
            "The goal is to get more detail about the target user, primary goals, and key features."
        )

    def execute(self, initial_prompt: str) -> str:
        """
        Takes an initial prompt and generates clarifying questions using an LLM.
        """
        print("Executing Clarifier Agent...")
        result = self._agent(
            f"Here is the user's initial idea: '{initial_prompt}'. "
            "Please generate clarifying questions."
        )
        return str(result)  # type: ignore
