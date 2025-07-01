from typing import List, Dict, Optional
import json
from strands import Agent
from deep_research_agent.agents.base_agent import BaseAgent
from deep_research_agent.services.prompt_service import PromptService
from deep_research_agent.common.schemas import AgentType
from deep_research_agent.utils.logger import logger


class ReportSynthesizerAgent(BaseAgent):
    def __init__(self, prompt_service: PromptService, agent: Optional[Agent] = None, model_id: Optional[str] = None):
        super().__init__(agent, model_id)
        self.prompt_service = prompt_service
        self._agent.system_prompt = self.prompt_service.get_system_prompt(AgentType.REPORT_SYNTHESIZER)

    def execute(self, ranked_list: List[Dict], creative_brief: str) -> str:
        """
        Compiles the final report with justifications and visualizations.
        """
        logger.info("Executing Report Synthesizer Agent...")
        
        # Convert the ranked list to a JSON string to pass to the LLM
        ranked_list_json = json.dumps(ranked_list, indent=2)

        user_prompt = self.prompt_service.format_user_prompt(
            AgentType.REPORT_SYNTHESIZER,
            "synthesize",
            creative_brief=creative_brief,
            ranked_list_json=ranked_list_json
        )
        
        report = self._agent(user_prompt)
        return str(report)  # type: ignore
