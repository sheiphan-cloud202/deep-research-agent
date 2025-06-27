from typing import Optional
from strands import Agent
from deep_research_agent.agents.base_agent import BaseAgent
from deep_research_agent.schemas import UseCases


class IdeationAgent(BaseAgent):
    def __init__(self, agent: Optional[Agent] = None, model_id: Optional[str] = None):
        super().__init__(agent, model_id)
        self._agent.system_prompt = (
            "You are an Ideation Agent. Your job is to generate creative, actionable use case ideas "
            "based on a 'Creative Brief'. The ideas should be distinct and grounded in the brief. "
            "If you receive feedback on initial ideas, your job is to refine them to address the feedback. "
            "You must generate exactly 10 use cases."
        )

    def execute(
        self, creative_brief: str, feedback: Optional[str] = None
    ) -> UseCases:
        """
        Generates or refines ideas based on a creative brief and optional feedback.
        """
        if feedback:
            print("Executing Ideation Agent (Refinement Pass)...")
            prompt = (
                f"Here is the creative brief:\n\n{creative_brief}\n\n"
                "We have received the following critical feedback on our initial ideas:\n"
                f"{feedback}\n\nPlease generate a new, refined list of 10 use cases that address this feedback."
            )
            result = self._agent.structured_output(UseCases, prompt)
            return result
        else:
            print("Executing Ideation Agent (Initial Pass)...")
            prompt = (
                "Based on the following creative brief, please generate a list of 10 high-level, "
                f"distinct use case ideas.\n\nCreative Brief:\n{creative_brief}"
            )
            result = self._agent.structured_output(UseCases, prompt)
            return result
