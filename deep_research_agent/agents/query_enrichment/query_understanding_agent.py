from typing import Any

from deep_research_agent.agents.base_agent import BaseAgent
from deep_research_agent.common.schemas import AgentType, MissionBrief
from deep_research_agent.core.agent_factory import AgentFactory
from deep_research_agent.services.prompt_service import PromptService
from deep_research_agent.utils.logger import logger


class QueryUnderstandingAgent(BaseAgent):
    def __init__(self, prompt_service: PromptService, model_id: str | None = None):
        super().__init__(prompt_service)
        self._agent = AgentFactory.create_agent(model_id)
        if self.prompt_service:
            self._agent.system_prompt = self.prompt_service.get_system_prompt(AgentType.QUERY_UNDERSTANDING)

    def execute(self, context: dict[str, Any]):
        if not self.prompt_service:
            raise ValueError("PromptService is not available for QueryUnderstandingAgent")

        prompt = self.prompt_service.format_user_prompt(
            AgentType.QUERY_UNDERSTANDING,
            "analyze",
            enhanced_prompt=context["enhanced_prompt"],
        )
        result = self._agent.structured_output(MissionBrief, prompt)
        context["mission_brief"] = result
        logger.info(f"Mission Brief:\n{result.model_dump_json(indent=2)}\n")
