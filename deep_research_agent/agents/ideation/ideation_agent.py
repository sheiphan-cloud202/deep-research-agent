from typing import List, Optional
from strands import Agent
from deep_research_agent.agents.base_agent import BaseAgent


class IdeationAgent(BaseAgent):
    def __init__(self, agent: Agent):
        super().__init__(agent)
        self._agent.system_prompt = (
            "You are an Ideation Agent. Your job is to generate creative, actionable use case ideas "
            "based on a 'Creative Brief'. The ideas should be distinct and grounded in the brief. "
            "If you receive feedback on initial ideas, your job is to refine them to address the feedback."
        )

    def execute(
        self, creative_brief: str, feedback: Optional[str] = None
    ) -> List[str]:
        """
        Generates or refines ideas based on a creative brief and optional feedback.
        """
        if feedback:
            print("Executing Ideation Agent (Refinement Pass)...")
            prompt = (
                f"Here is the creative brief:\n\n{creative_brief}\n\n"
                "We have received the following critical feedback on our initial ideas:\n"
                f"{feedback}\n\nPlease generate a new, refined list of 2-3 ideas that address this feedback."
            )
            result = self._agent(prompt)
            # Assuming the result is a newline-separated list of ideas
            return str(result).strip().split('\n')
        else:
            print("Executing Ideation Agent (Initial Pass)...")
            prompt = (
                "Based on the following creative brief, please generate a list of 2-3 high-level, "
                f"distinct use case ideas.\n\nCreative Brief:\n{creative_brief}"
            )
            result = self._agent(prompt)
            # Assuming the result is a newline-separated list of ideas
            return str(result).strip().split('\n')
