from typing import List, Optional
from strands import Agent
from deep_research_agent.agents.base_agent import BaseAgent
from deep_research_agent.prompt_service import PromptService, AgentType


class DevilsAdvocateAgent(BaseAgent):
    def __init__(self, agent: Optional[Agent] = None, model_id: Optional[str] = None):
        super().__init__(agent, model_id)
        self._agent.system_prompt = PromptService.get_system_prompt(AgentType.DEVILS_ADVOCATE)

    def execute(self, ideas: List[str]) -> str:
        """
        Critiques a list of ideas to find weaknesses.
        """
        print("Executing Devil's Advocate Agent...")
        ideas_str = "\n".join(f"- {idea}" for idea in ideas)
        user_prompt = PromptService.format_user_prompt(
            AgentType.DEVILS_ADVOCATE,
            "critique",
            ideas_str=ideas_str
        )
        result = self._agent(user_prompt)
        return str(result)  # type: ignore
