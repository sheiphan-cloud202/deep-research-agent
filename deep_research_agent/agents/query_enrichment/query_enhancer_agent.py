from typing import Any

from deep_research_agent.agents.base_agent import BaseAgent
from deep_research_agent.common.config import settings
from deep_research_agent.common.schemas import AgentType
from deep_research_agent.core.agent_factory import AgentFactory
from deep_research_agent.services.prompt_service import PromptService
from deep_research_agent.utils.logger import logger


class QueryEnhancerAgent(BaseAgent):
    def __init__(self, prompt_service: PromptService, model_id: str | None = None):
        super().__init__(prompt_service)
        self._agent = AgentFactory.create_agent(model_id or settings.claude_3_5_sonnet_model_id)
        if self.prompt_service:
            self._agent.system_prompt = self.prompt_service.get_system_prompt(AgentType.QUERY_ENHANCER)

    def execute(self, context: dict[str, Any]):
        if not self.prompt_service:
            raise ValueError("PromptService is not available for QueryEnhancerAgent")

        prompt = self.prompt_service.format_user_prompt(
            AgentType.QUERY_ENHANCER, "enhance", summary=context["summary"]
        )
        result = self._agent(prompt)
        context["enhanced_prompt"] = str(result)
        logger.info(f"Enhanced Prompt:\n{result}\n")
