from typing import List, Dict, Optional
import json
from strands import Agent
from deep_research_agent.agents.base_agent import BaseAgent
from deep_research_agent.prompt_service import PromptService, AgentType


class ReportSynthesizerAgent(BaseAgent):
    def __init__(self, agent: Optional[Agent] = None, model_id: Optional[str] = None):
        super().__init__(agent, model_id)
        self._agent.system_prompt = PromptService.get_system_prompt(AgentType.REPORT_SYNTHESIZER)

    def execute(self, ranked_list: List[Dict], creative_brief: str) -> str:
        """
        Compiles the final report with justifications and visualizations.
        """
        print("Executing Report Synthesizer Agent...")
        
        # Convert the ranked list to a JSON string to pass to the LLM
        ranked_list_json = json.dumps(ranked_list, indent=2)

        user_prompt = PromptService.format_user_prompt(
            AgentType.REPORT_SYNTHESIZER,
            "synthesize",
            creative_brief=creative_brief,
            ranked_list_json=ranked_list_json
        )
        
        report = self._agent(user_prompt)
        return str(report)  # type: ignore
