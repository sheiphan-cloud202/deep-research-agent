from typing import List
from strands import Agent
from deep_research_agent.agents.base_agent import BaseAgent


class SearchSummarizerAgent(BaseAgent):
    def __init__(self, agent: Agent):
        super().__init__(agent)
        self._agent.system_prompt = (
            "You are a Search Summarizer Agent. Your job is to synthesize multiple research reports "
            "and user personas into a single, well-structured 'Creative Brief' in Markdown format. "
            "This brief should highlight the key market context, clinical findings, emerging trends, and user personas."
        )

    def execute(self, research_reports: List[str]) -> str:
        """
        Summarizes multiple research reports into a 'Creative Brief'.
        """
        print("Executing Search Summarizer Agent...")
        reports_str = "\n\n---\n\n".join(research_reports)
        result = self._agent(
            "Please synthesize the following research reports and user personas into a "
            f"cohesive 'Creative Brief' in Markdown format:\n\n{reports_str}"
        )
        return str(result)  # type: ignore
