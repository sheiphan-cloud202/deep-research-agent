from typing import List, Optional
from strands import Agent
from deep_research_agent.agents.base_agent import BaseAgent
from deep_research_agent.services.prompt_service import PromptService
from deep_research_agent.common.schemas import AgentType
from deep_research_agent.utils.logger import logger


class SearchSummarizerAgent(BaseAgent):
    def __init__(self, prompt_service: PromptService, agent: Optional[Agent] = None, model_id: Optional[str] = None):
        super().__init__(agent, model_id)
        self.prompt_service = prompt_service
        self._agent.system_prompt = self.prompt_service.get_system_prompt(AgentType.SEARCH_SUMMARIZER)

    def execute(self, research_reports: List[str]) -> str:
        """
        Summarizes multiple research reports into a 'Creative Brief'.
        """
        logger.info("Executing Search Summarizer Agent...")
        reports_str = "\n\n---\n\n".join(research_reports)
        user_prompt = self.prompt_service.format_user_prompt(
            AgentType.SEARCH_SUMMARIZER,
            "summarize_reports",
            reports_str=reports_str
        )
        result = self._agent(user_prompt)
        return str(result)  # type: ignore
