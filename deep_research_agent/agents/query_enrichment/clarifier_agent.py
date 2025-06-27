from strands import Agent
from typing import Optional
from deep_research_agent.agents.base_agent import BaseAgent


class ClarifierAgent(BaseAgent):
    def __init__(self, agent: Optional[Agent] = None, model_id: Optional[str] = None):
        super().__init__(agent, model_id)
        self._agent.system_prompt = (
            "You are a Clarifier Agent. Your job is to analyze a user's prompt "
            "and ask 2-3 specific, targeted questions to help refine their idea. "
            "The goal is to get more detail about the target user, primary goals, and key features. "
            "When the user is ready to proceed, they will say 'start the agent', 'yes', 'run', "
            "'start agent', 'begin', or 'go'. Continue the conversation until they use one of these trigger words."
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

    def execute_interactive(self, latest_context: str, full_context: str) -> str:
        """
        Generate clarifying questions based on ongoing conversation context.
        """
        result = self._agent(
            f"Here is the conversation so far: '{full_context}'. "
            f"The user's latest response was: '{latest_context}'. "
            "Based on this conversation, please ask 1-2 thoughtful follow-up questions "
            "to help refine and clarify their idea further. Keep the questions focused "
            "and avoid repeating information already covered."
        )
        return str(result)  # type: ignore
