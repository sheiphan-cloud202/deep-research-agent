from typing import Any

from deep_research_agent.agents.base_agent import BaseAgent
from deep_research_agent.common.config import settings
from deep_research_agent.common.schemas import AgentType, UseCases
from deep_research_agent.core.agent_factory import AgentFactory
from deep_research_agent.services.prompt_service import PromptService
from deep_research_agent.utils.logger import logger


class IdeationAgent(BaseAgent):
    def __init__(self, prompt_service: PromptService, model_id: str | None = None):
        super().__init__(prompt_service)
        self._agent = AgentFactory.create_agent(model_id or settings.claude_3_5_sonnet_model_id)
        if self.prompt_service:
            self._agent.system_prompt = self.prompt_service.get_system_prompt(AgentType.IDEATION)

    def execute(self, context: dict[str, Any]):
        if not self.prompt_service:
            raise ValueError("PromptService is not available for IdeationAgent")

        creative_brief = context["creative_brief"]
        feedback = context.get("devils_advocate_feedback")

        if feedback:
            # This is the second pass, refining ideas
            prompt = self.prompt_service.format_user_prompt(
                AgentType.IDEATION,
                "refine_with_feedback",
                creative_brief=creative_brief,
                feedback=feedback,
            )
            result = self._agent.structured_output(UseCases, prompt)
            context["refined_ideas"] = result
            logger.info(f"Refined Ideas:\n{result.model_dump_json(indent=2)}\n")
        else:
            # This is the first pass, generating initial ideas
            prompt = self.prompt_service.format_user_prompt(
                AgentType.IDEATION, "generate_initial", creative_brief=creative_brief
            )
            result = self._agent.structured_output(UseCases, prompt)
            context["initial_ideas"] = result
            logger.info(f"Initial Ideas:\n{result.model_dump_json(indent=2)}\n")
