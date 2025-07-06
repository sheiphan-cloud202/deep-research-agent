from typing import Any, cast

from deep_research_agent.agents.base_agent import BaseAgent
from deep_research_agent.common.config import settings
from deep_research_agent.common.schemas import AgentType, UseCases
from deep_research_agent.core.agent_factory import AgentFactory
from deep_research_agent.services.prompt_service import PromptService
from deep_research_agent.utils.logger import logger


class DevilsAdvocateAgent(BaseAgent):
    def __init__(self, prompt_service: PromptService, model_id: str | None = None):
        super().__init__(prompt_service)
        self._agent = AgentFactory.create_agent(model_id or settings.claude_3_5_sonnet_model_id)
        if self.prompt_service:
            self._agent.system_prompt = self.prompt_service.get_system_prompt(AgentType.DEVILS_ADVOCATE)

    def execute(self, context: dict[str, Any]):
        if not self.prompt_service:
            raise ValueError("PromptService is not available for DevilsAdvocateAgent")

        initial_ideas = cast(UseCases, context["initial_ideas"])
        idea_list = [f"- {i.name}: {i.description}" for i in initial_ideas.use_cases]
        ideas_str = "\n".join(idea_list)

        prompt = self.prompt_service.format_user_prompt(AgentType.DEVILS_ADVOCATE, "critique", ideas_str=ideas_str)
        result = self._agent(prompt)
        context["devils_advocate_feedback"] = str(result)
        logger.info(f"Devil's Advocate Feedback:\n{result}\n")
