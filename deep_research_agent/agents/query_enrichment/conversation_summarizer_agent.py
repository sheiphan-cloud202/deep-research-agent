from typing import List
from strands import Agent
from deep_research_agent.agents.base_agent import BaseAgent


class ConversationSummarizerAgent(BaseAgent):
    def __init__(self, agent: Agent):
        super().__init__(agent)
        self._agent.system_prompt = (
            "You are a Conversation Summarizer Agent. Your job is to take a conversation history "
            "(a list of utterances) and summarize it into a single, cohesive paragraph. "
            "Focus on capturing the user's core need and the refined requirements."
        )

    def execute(self, conversation_history: List[str]) -> str:
        """
        Summarizes a conversation history into a single paragraph.
        """
        print("Executing Conversation Summarizer Agent...")
        history_str = "\n".join(conversation_history)
        result = self._agent(
            f"Please summarize the following conversation into one paragraph:\n\n{history_str}"
        )
        return str(result)  # type: ignore
