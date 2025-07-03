from strands import Agent

from deep_research_agent.agents.base_agent import BaseAgent
from deep_research_agent.common.schemas import AgentType
from deep_research_agent.services.prompt_service import PromptService
from deep_research_agent.utils.logger import logger


class ClarifierAgent(BaseAgent):
    def __init__(
        self,
        prompt_service: PromptService,
        agent: Agent | None = None,
        model_id: str | None = None,
    ):
        super().__init__(agent, model_id)
        self.prompt_service = prompt_service
        self._agent.system_prompt = self.prompt_service.get_system_prompt(AgentType.CLARIFIER)

    def execute(self, initial_prompt: str, full_conversation: str) -> str:
        """
        Takes an initial prompt and generates clarifying questions using an LLM.
        """
        logger.info("Executing Clarifier Agent...")
        user_prompt = self.prompt_service.format_user_prompt(
            AgentType.CLARIFIER, "clarify", initial_prompt=initial_prompt
        )
        result = self._agent(user_prompt)
        return str(result)  # type: ignore

    def execute_interactive(self, latest_context: str, full_context: str) -> str:
        """
        Generate clarifying questions based on ongoing conversation context.
        """
        user_prompt = self.prompt_service.format_user_prompt(
            AgentType.CLARIFIER,
            "interactive",
            latest_context=latest_context,
            full_context=full_context,
        )
        result = self._agent(user_prompt)
        return str(result)  # type: ignore
