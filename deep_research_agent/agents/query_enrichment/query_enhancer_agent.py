from strands import Agent

from deep_research_agent.agents.base_agent import BaseAgent
from deep_research_agent.common.schemas import AgentType
from deep_research_agent.services.prompt_service import PromptService
from deep_research_agent.utils.logger import logger


class QueryEnhancerAgent(BaseAgent):
    def __init__(
        self,
        prompt_service: PromptService,
        agent: Agent | None = None,
        model_id: str | None = None,
    ):
        super().__init__(agent, model_id)
        self.prompt_service = prompt_service
        self._agent.system_prompt = self.prompt_service.get_system_prompt(AgentType.QUERY_ENHANCER)

    def execute(self, summary: str) -> str:
        """
        Enhances a conversation summary into a formal, actionable prompt.
        """
        logger.info("Executing Query Enhancer Agent...")
        user_prompt = self.prompt_service.format_user_prompt(AgentType.QUERY_ENHANCER, "enhance", summary=summary)
        result = self._agent(user_prompt)
        return str(result)  # type: ignore
