from typing import Any, cast

from deep_research_agent.agents.base_agent import BaseAgent
from deep_research_agent.common.config import settings
from deep_research_agent.common.schemas import AgentType, UseCases
from deep_research_agent.core.agent_factory import AgentFactory
from deep_research_agent.services.prompt_service import PromptService
from deep_research_agent.utils.logger import logger

from .ethical_guardian_agent import EthicalGuardianAgent
from .market_viability_agent import MarketViabilityAgent
from .technical_feasibility_agent import TechnicalFeasibilityAgent


class EvaluationCoordinatorAgent(BaseAgent):
    def __init__(self, prompt_service: PromptService, model_id: str | None = None):
        super().__init__(prompt_service)
        self._agent = AgentFactory.create_agent(model_id or settings.claude_3_5_sonnet_model_id)
        if self.prompt_service:
            self._agent.system_prompt = self.prompt_service.get_system_prompt(AgentType.EVALUATION_COORDINATOR)

        self.technical_feasibility_agent = TechnicalFeasibilityAgent(prompt_service, model_id=model_id)
        self.ethical_guardian_agent = EthicalGuardianAgent(prompt_service, model_id=model_id)
        self.market_viability_agent = MarketViabilityAgent(prompt_service, model_id=model_id)

    def execute(self, context: dict[str, Any]):
        if not self.prompt_service:
            raise ValueError("PromptService is not available for EvaluationCoordinatorAgent")

        refined_ideas = cast(UseCases, context["initial_ideas"])
        idea_list = [f"{i.name}: {i.description}" for i in refined_ideas.use_cases]
        result = self.execute_agent(idea_list)
        context["scored_ideas"] = result

    def execute_agent(self, ideas: list[str]):
        all_scores = {}
        for idea in ideas:
            logger.info(f"Coordinating evaluation for idea: {idea}")
            idea_scores = []

            # Get scores from each specialist agent
            tech_score = self.technical_feasibility_agent.execute(idea)
            idea_scores.append(tech_score)

            # ethical_score = self.ethical_guardian_agent.execute(idea)
            # idea_scores.append(ethical_score)

            # market_score = self.market_viability_agent.execute(idea)
            # idea_scores.append(market_score)

            all_scores[idea] = idea_scores

        return all_scores
