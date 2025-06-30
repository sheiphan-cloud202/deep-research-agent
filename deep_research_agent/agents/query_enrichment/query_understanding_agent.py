from strands import Agent
from typing import Optional

from deep_research_agent.agents.base_agent import BaseAgent
from deep_research_agent.schemas import MissionBrief, Filters, DecomposedTasks
from deep_research_agent.prompt_service import PromptService, AgentType


class QueryUnderstandingAgent(BaseAgent):
    def __init__(self, agent: Optional[Agent] = None, model_id: Optional[str] = None):
        super().__init__(agent, model_id)
        self._agent.system_prompt = PromptService.get_system_prompt(AgentType.QUERY_UNDERSTANDING)

    def execute(self, enhanced_prompt: str) -> MissionBrief:
        """
        Converts an enhanced prompt into a structured JSON Mission Brief
        using a large language model.
        """
        print("Executing Query Understanding Agent...")
        user_prompt = PromptService.format_user_prompt(
            AgentType.QUERY_UNDERSTANDING,
            "analyze",
            enhanced_prompt=enhanced_prompt
        )
        mission_brief = self._agent.structured_output(MissionBrief, user_prompt)
        return mission_brief
