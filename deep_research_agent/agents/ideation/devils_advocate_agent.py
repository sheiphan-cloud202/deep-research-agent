from strands import Agent

from deep_research_agent.agents.base_agent import BaseAgent
from deep_research_agent.common.schemas import AgentType
from deep_research_agent.services.prompt_service import PromptService
from deep_research_agent.utils.logger import logger


class DevilsAdvocateAgent(BaseAgent):
    def __init__(
        self,
        prompt_service: PromptService,
        agent: Agent | None = None,
        model_id: str | None = None,
    ):
        super().__init__(agent, model_id)
        self.prompt_service = prompt_service
        self._agent.system_prompt = self.prompt_service.get_system_prompt(AgentType.DEVILS_ADVOCATE)

    def execute(self, ideas: list[str]) -> str:
        """
        Critiques a list of ideas to find weaknesses.
        """
        logger.info("Executing Devil's Advocate Agent...")
        ideas_str = "\n".join(f"- {idea}" for idea in ideas)
        user_prompt = self.prompt_service.format_user_prompt(
            AgentType.DEVILS_ADVOCATE, "critique", ideas_str=ideas_str
        )
        result = self._agent(user_prompt)
        return str(result)  # type: ignore
