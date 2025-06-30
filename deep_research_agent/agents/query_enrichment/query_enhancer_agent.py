from strands import Agent
from typing import Optional
from deep_research_agent.agents.base_agent import BaseAgent
from deep_research_agent.prompt_service import PromptService, AgentType


class QueryEnhancerAgent(BaseAgent):
    def __init__(self, agent: Optional[Agent] = None, model_id: Optional[str] = None):
        super().__init__(agent, model_id)
        self._agent.system_prompt = PromptService.get_system_prompt(AgentType.QUERY_ENHANCER)

    def execute(self, summary: str) -> str:
        """
        Enhances a conversation summary into a formal, actionable prompt.
        """
        print("Executing Query Enhancer Agent...")
        user_prompt = PromptService.format_user_prompt(
            AgentType.QUERY_ENHANCER,
            "enhance",
            summary=summary
        )
        result = self._agent(user_prompt)
        return str(result)  # type: ignore
