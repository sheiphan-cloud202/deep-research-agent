from strands import Agent

from deep_research_agent.agents.base_agent import BaseAgent
from deep_research_agent.common.config import settings
from deep_research_agent.common.schemas import EvaluationScore
from deep_research_agent.core.agent_factory import AgentFactory
from deep_research_agent.services.prompt_service import AgentType, PromptService
from deep_research_agent.utils.logger import logger


class EthicalGuardianAgent(BaseAgent):
    def __init__(
        self,
        prompt_service: PromptService,
        model_id: str | None = None,
    ):
        super().__init__(prompt_service)
        self._agent: Agent = AgentFactory.create_agent(model_id or settings.claude_3_5_sonnet_model_id)
        if self.prompt_service:
            self._agent.system_prompt = self.prompt_service.get_system_prompt(AgentType.ETHICAL_GUARDIAN)

    def execute(self, idea: str) -> EvaluationScore:
        """
        Scores an idea for safety, fairness, and bias.
        """
        if not self.prompt_service:
            raise ValueError("PromptService is not available for EthicalGuardianAgent")

        logger.info(f"Executing Ethical Guardian Agent for: {idea}")

        user_prompt = self.prompt_service.format_user_prompt(AgentType.ETHICAL_GUARDIAN, "evaluate", idea=idea)

        score = self._agent.structured_output(EvaluationScore, user_prompt)
        score.agent = self.__class__.__name__
        return score
