from strands import Agent

from deep_research_agent.agents.base_agent import BaseAgent
from deep_research_agent.schemas import MissionBrief, Filters, DecomposedTasks


class QueryUnderstandingAgent(BaseAgent):
    def __init__(self, agent: Agent):
        super().__init__(agent)
        self._agent.system_prompt = (
            "You are a Query Understanding Agent. Your job is to analyze an enhanced prompt "
            "and convert it into a structured JSON Mission Brief. You must identify the main topic, "
            "industry, relevant tools, and decompose the main query into sub-tasks for other agents."
        )

    def execute(self, enhanced_prompt: str) -> MissionBrief:
        """
        Converts an enhanced prompt into a structured JSON Mission Brief
        using a large language model.
        """
        print("Executing Query Understanding Agent...")
        mission_brief = self._agent.structured_output(
            MissionBrief,
            f"Analyze the following user mission and extract the key components into the required format. "
            f"Here is the mission: '{enhanced_prompt}'",
        )
        return mission_brief
