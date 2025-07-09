from typing import Any

from deep_research_agent.agents.base_agent import BaseAgent
from deep_research_agent.common.schemas import AgentType, AwaitingUserInputError
from deep_research_agent.core.agent_factory import AgentFactory
from deep_research_agent.services.prompt_service import PromptService
from deep_research_agent.utils.logger import logger


class ClarifierAgent(BaseAgent):
    def __init__(self, prompt_service: PromptService, model_id: str | None = None):
        super().__init__(prompt_service)
        self._agent = AgentFactory.create_agent(model_id)
        if self.prompt_service:
            self._agent.system_prompt = self.prompt_service.get_system_prompt(AgentType.CLARIFIER)

    def execute(self, context: dict[str, Any]):
        if not self.prompt_service:
            raise ValueError("PromptService is not available for ClarifierAgent")

        conversation_history = context.get("conversation_history", [])
        if not conversation_history:
            logger.warning("ClarifierAgent expects 'conversation_history' in the context, but it was empty.")
            return

        trigger_words = [
            "start the agent",
            "yes",
            "run",
            "start agent",
            "begin",
            "go",
        ]
        latest_user_response = conversation_history[-1]

        if any(trigger.lower() in latest_user_response.lower() for trigger in trigger_words):
            logger.info("\n✅ Great! Moving to the next step...\n")
            return

        logger.info("\n💭 Let me ask you some clarifying questions to better understand your idea...\n")

        latest_context = conversation_history[-1]
        full_context = "\n".join(conversation_history)

        prompt = self.prompt_service.format_user_prompt(
            AgentType.CLARIFIER,
            "interactive",
            latest_context=latest_context,
            full_context=full_context,
        )
        clarifying_questions = self._agent(prompt)
        logger.info(f"🤔 {clarifying_questions}\n")

        raise AwaitingUserInputError(str(clarifying_questions))
