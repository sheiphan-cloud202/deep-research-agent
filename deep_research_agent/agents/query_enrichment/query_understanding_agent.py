from strands import Agent

from deep_research_agent.agents.base_agent import BaseAgent
from deep_research_agent.common.schemas import MissionBrief
from deep_research_agent.services.prompt_service import AgentType, PromptService
from deep_research_agent.utils.logger import logger


class QueryUnderstandingAgent(BaseAgent):
    def __init__(
        self,
        prompt_service: PromptService,
        agent: Agent | None = None,
        model_id: str | None = None,
    ):
        super().__init__(agent, model_id)
        self.prompt_service = prompt_service
        self._agent.system_prompt = self.prompt_service.get_system_prompt(AgentType.QUERY_UNDERSTANDING)

    def execute(self, enhanced_prompt: str) -> MissionBrief:
        """
        Converts an enhanced prompt into a structured JSON Mission Brief
        using a large language model.
        """
        logger.info("Executing Query Understanding Agent...")
        user_prompt = self.prompt_service.format_user_prompt(
            AgentType.QUERY_UNDERSTANDING, "analyze", enhanced_prompt=enhanced_prompt
        )
        mission_brief = self._agent.structured_output(MissionBrief, user_prompt)
        return mission_brief
