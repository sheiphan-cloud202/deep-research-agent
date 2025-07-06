import json
from typing import Any

from deep_research_agent.agents.base_agent import BaseAgent
from deep_research_agent.common.schemas import AgentType
from deep_research_agent.core.agent_factory import AgentFactory
from deep_research_agent.services.prompt_service import PromptService


class ReportSynthesizerAgent(BaseAgent):
    def __init__(self, prompt_service: PromptService, model_id: str | None = None):
        super().__init__(prompt_service)
        self._agent = AgentFactory.create_agent(model_id)
        if self.prompt_service:
            self._agent.system_prompt = self.prompt_service.get_system_prompt(AgentType.REPORT_SYNTHESIZER)

    def execute(self, context: dict[str, Any]):
        if not self.prompt_service:
            raise ValueError("PromptService is not available for ReportSynthesizerAgent")

        serializable_ranked_list = self._serialize_ranked_ideas(context["ranked_ideas"])
        ranked_list_json = json.dumps(serializable_ranked_list, indent=2)
        prompt = self.prompt_service.format_user_prompt(
            AgentType.REPORT_SYNTHESIZER,
            "synthesize",
            ranked_list_json=ranked_list_json,
            creative_brief=context["creative_brief"],
        )
        result = self._agent(prompt)
        context["final_report"] = str(result)

    def _serialize_ranked_ideas(self, ranked_ideas: list[tuple[str, list[Any]]]) -> list[dict[str, Any]]:
        serializable_list = []
        for idea, scores in ranked_ideas:
            serializable_scores = [score.model_dump() if hasattr(score, "model_dump") else score for score in scores]
            serializable_list.append({"idea": idea, "scores": serializable_scores})
        return serializable_list
