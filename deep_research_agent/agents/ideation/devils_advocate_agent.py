from typing import List
from strands import Agent
from deep_research_agent.agents.base_agent import BaseAgent


class DevilsAdvocateAgent(BaseAgent):
    def __init__(self, agent: Agent):
        super().__init__(agent)
        self._agent.system_prompt = (
            "You are a Devil's Advocate Agent. Your role is to be a critical, constructive challenger. "
            "Analyze a list of ideas and provide sharp, insightful critiques for each one, pointing out "
            "potential weaknesses, unstated assumptions, or user adoption issues. Frame your output as a list of critiques."
        )

    def execute(self, ideas: List[str]) -> str:
        """
        Critiques a list of ideas to find weaknesses.
        """
        print("Executing Devil's Advocate Agent...")
        ideas_str = "\n".join(f"- {idea}" for idea in ideas)
        result = self._agent(
            "Please act as a devil's advocate and provide critical feedback for the following "
            f"ideas:\n{ideas_str}"
        )
        return str(result)  # type: ignore
