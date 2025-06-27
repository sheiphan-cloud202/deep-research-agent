from typing import List, Dict, Optional
from strands import Agent
from deep_research_agent.agents.base_agent import BaseAgent
from deep_research_agent.schemas import EvaluationScore


class RankingAgent(BaseAgent):
    def __init__(self, agent: Optional[Agent] = None, model_id: Optional[str] = None):
        super().__init__(agent, model_id)
        # This agent performs a deterministic ranking, so the LLM agent is not used,
        # but we adhere to the BaseAgent pattern.

    def execute(self, scored_ideas: Dict[str, List[EvaluationScore]]) -> List[Dict]:
        """
        Consolidates scores and ranks all refined ideas.
        """
        print("Executing Ranking Agent...")
        
        processed_data = []
        for idea, scores in scored_ideas.items():
            total_score = sum(item.score for item in scores)
            avg_score = total_score / len(scores) if scores else 0
            processed_data.append({
                "idea": idea,
                "overall_score": round(avg_score, 2),
                "scores": [score.model_dump() for score in scores],  # Convert back to dict for output
            })
        
        # Rank based on overall score
        ranked_list = sorted(processed_data, key=lambda x: x['overall_score'], reverse=True)
        
        print("Ranked List:")
        for item in ranked_list:
            print(f"- {item['idea']} (Overall Score: {item['overall_score']})")
            
        return ranked_list
