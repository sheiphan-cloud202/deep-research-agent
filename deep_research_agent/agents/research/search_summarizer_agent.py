from typing import List, Optional
from strands import Agent
from deep_research_agent.agents.base_agent import BaseAgent
from deep_research_agent.prompt_service import PromptService, AgentType


class SearchSummarizerAgent(BaseAgent):
    def __init__(self, agent: Optional[Agent] = None, model_id: Optional[str] = None):
        super().__init__(agent, model_id)
        self._agent.system_prompt = PromptService.get_system_prompt(AgentType.SEARCH_SUMMARIZER)

    def execute(self, research_reports: List[str]) -> str:
        """
        Summarizes multiple research reports into a 'Creative Brief'.
        """
        print("Executing Search Summarizer Agent...")
        reports_str = "\n\n---\n\n".join(research_reports)
        user_prompt = PromptService.format_user_prompt(
            AgentType.SEARCH_SUMMARIZER,
            "summarize_reports",
            reports_str=reports_str
        )
        result = self._agent(user_prompt)
        return str(result)  # type: ignore
