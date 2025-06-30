from strands import Agent
from typing import Optional
from deep_research_agent.agents.base_agent import BaseAgent
from deep_research_agent.prompt_service import PromptService, AgentType


class ClarifierAgent(BaseAgent):
    def __init__(self, agent: Optional[Agent] = None, model_id: Optional[str] = None):
        super().__init__(agent, model_id)
        self._agent.system_prompt = PromptService.get_system_prompt(AgentType.CLARIFIER)

    def execute(self, initial_prompt: str) -> str:
        """
        Takes an initial prompt and generates clarifying questions using an LLM.
        """
        print("Executing Clarifier Agent...")
        user_prompt = PromptService.format_user_prompt(
            AgentType.CLARIFIER,
            "clarify",
            initial_prompt=initial_prompt
        )
        result = self._agent(user_prompt)
        return str(result)  # type: ignore

    def execute_interactive(self, latest_context: str, full_context: str) -> str:
        """
        Generate clarifying questions based on ongoing conversation context.
        """
        user_prompt = PromptService.format_user_prompt(
            AgentType.CLARIFIER,
            "interactive",
            latest_context=latest_context,
            full_context=full_context
        )
        result = self._agent(user_prompt)
        return str(result)  # type: ignore
