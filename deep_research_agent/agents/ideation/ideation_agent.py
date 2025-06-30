from typing import Optional
from strands import Agent
from deep_research_agent.agents.base_agent import BaseAgent
from deep_research_agent.schemas import UseCases
from deep_research_agent.prompt_service import PromptService, AgentType


class IdeationAgent(BaseAgent):
    def __init__(self, agent: Optional[Agent] = None, model_id: Optional[str] = None):
        super().__init__(agent, model_id)
        self._agent.system_prompt = PromptService.get_system_prompt(AgentType.IDEATION)

    def execute(
        self, creative_brief: str, feedback: Optional[str] = None
    ) -> UseCases:
        """
        Generates or refines ideas based on a creative brief and optional feedback.
        """
        if feedback:
            print("Executing Ideation Agent (Refinement Pass)...")
            prompt = PromptService.format_user_prompt(
                AgentType.IDEATION,
                "refine_with_feedback",
                creative_brief=creative_brief,
                feedback=feedback
            )
            result = self._agent.structured_output(UseCases, prompt)
            return result
        else:
            print("Executing Ideation Agent (Initial Pass)...")
            prompt = PromptService.format_user_prompt(
                AgentType.IDEATION,
                "generate_initial",
                creative_brief=creative_brief
            )
            result = self._agent.structured_output(UseCases, prompt)
            return result
