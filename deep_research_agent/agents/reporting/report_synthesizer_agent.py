from typing import List, Dict
import json
from strands import Agent
from deep_research_agent.agents.base_agent import BaseAgent


class ReportSynthesizerAgent(BaseAgent):
    def __init__(self, agent: Agent):
        super().__init__(agent)
        self._agent.system_prompt = (
            "You are a Report Synthesizer Agent. Your job is to create a final, comprehensive, and well-structured "
            "report in Markdown format. The report should summarize the entire research and ideation process, "
            "highlighting the top-ranked idea, its scores, and the justification for its ranking. "
            "Use the provided creative brief and ranked list of ideas to generate the report."
        )

    def execute(self, ranked_list: List[Dict], creative_brief: str) -> str:
        """
        Compiles the final report with justifications and visualizations.
        """
        print("Executing Report Synthesizer Agent...")
        
        # Convert the ranked list to a JSON string to pass to the LLM
        ranked_list_json = json.dumps(ranked_list, indent=2)

        prompt = (
            "Please create a final, compelling report in Markdown format. "
            "The report should be based on the following creative brief and ranked list of ideas.\n\n"
            f"## Creative Brief\n{creative_brief}\n\n"
            f"## Ranked and Scored Ideas\n{ranked_list_json}\n\n"
            "The report should start with an executive summary, then detail the top-ranked idea, "
            "its scores, and a compelling justification. It should be professional and easy to read."
        )
        
        report = self._agent(prompt)
        return str(report)  # type: ignore
