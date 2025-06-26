from typing import List, Dict
from strands import Agent
from deep_research_agent.agents.base_agent import BaseAgent
from deep_research_agent.agents.evaluation.ethical_guardian_agent import EthicalGuardianAgent
from deep_research_agent.agents.evaluation.market_viability_agent import MarketViabilityAgent
from deep_research_agent.agents.evaluation.technical_feasibility_agent import TechnicalFeasibilityAgent


class EvaluationCoordinatorAgent(BaseAgent):
    def __init__(self, agent: Agent):
        super().__init__(agent)
        self._agent.system_prompt = (
            "You are an Evaluation Coordinator Agent. Your role is to manage the multi-faceted "
            "evaluation of a list of ideas by delegating to specialist evaluator agents."
        )
        # Specialist agents are initialized here
        self.technical_feasibility_agent = TechnicalFeasibilityAgent(agent)
        self.ethical_guardian_agent = EthicalGuardianAgent(agent)
        self.market_viability_agent = MarketViabilityAgent(agent)

    def execute(self, ideas: List[str]) -> Dict:
        """
        Coordinates the evaluation of ideas by specialist agents.
        """
        print("Executing Evaluation Coordinator Agent...")
        
        all_scores = {}
        for idea in ideas:
            print(f"Coordinating evaluation for idea: {idea}")
            idea_scores = []
            
            # Get scores from each specialist agent
            tech_score = self.technical_feasibility_agent.execute(idea)
            idea_scores.append(tech_score)
            
            ethical_score = self.ethical_guardian_agent.execute(idea)
            idea_scores.append(ethical_score)
            
            market_score = self.market_viability_agent.execute(idea)
            idea_scores.append(market_score)
            
            all_scores[idea] = idea_scores
            
        return all_scores
