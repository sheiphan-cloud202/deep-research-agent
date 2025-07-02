from strands import Agent

from deep_research_agent.agents.base_agent import BaseAgent
from deep_research_agent.agents.evaluation.ethical_guardian_agent import EthicalGuardianAgent
from deep_research_agent.agents.evaluation.market_viability_agent import MarketViabilityAgent
from deep_research_agent.agents.evaluation.technical_feasibility_agent import TechnicalFeasibilityAgent
from deep_research_agent.services.prompt_service import AgentType, PromptService
from deep_research_agent.utils.logger import logger


class EvaluationCoordinatorAgent(BaseAgent):
    def __init__(
        self,
        prompt_service: PromptService,
        agent: Agent | None = None,
        model_id: str | None = None,
    ):
        super().__init__(agent, model_id)
        self.prompt_service = prompt_service
        self._agent.system_prompt = self.prompt_service.get_system_prompt(AgentType.EVALUATION_COORDINATOR)
        # Specialist agents are initialized here
        self.technical_feasibility_agent = TechnicalFeasibilityAgent(
            prompt_service=self.prompt_service, agent=self._agent
        )
        self.ethical_guardian_agent = EthicalGuardianAgent(prompt_service=self.prompt_service, agent=self._agent)
        self.market_viability_agent = MarketViabilityAgent(prompt_service=self.prompt_service, agent=self._agent)

    def execute(self, ideas: list[str]) -> dict:
        """
        Coordinates the evaluation of ideas by specialist agents.
        """
        logger.info("Executing Evaluation Coordinator Agent...")

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
