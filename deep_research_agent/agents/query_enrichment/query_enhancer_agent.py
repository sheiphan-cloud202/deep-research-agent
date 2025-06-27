from strands import Agent
from typing import Optional
from deep_research_agent.agents.base_agent import BaseAgent


class QueryEnhancerAgent(BaseAgent):
    def __init__(self, agent: Optional[Agent] = None, model_id: Optional[str] = None):
        super().__init__(agent, model_id)
        self._agent.system_prompt = (
            "You are a Query Enhancer Agent. Your task is to take a summarized user request "
            "and transform it into a formal, actionable, and inspiring mission prompt for a team of AI agents. "
            "Start the prompt with 'Your mission is to:'"
        )

    def execute(self, summary: str) -> str:
        """
        Enhances a conversation summary into a formal, actionable prompt.
        """
        print("Executing Query Enhancer Agent...")
        result = self._agent(
            f"Please enhance the following summary into a formal mission prompt: '{summary}'"
        )
        return str(result)  # type: ignore
