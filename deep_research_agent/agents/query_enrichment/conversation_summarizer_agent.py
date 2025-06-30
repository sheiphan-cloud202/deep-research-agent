from typing import List, Optional
from strands import Agent
from deep_research_agent.agents.base_agent import BaseAgent
from deep_research_agent.prompt_service import PromptService, AgentType


class ConversationSummarizerAgent(BaseAgent):
    def __init__(self, agent: Optional[Agent] = None, model_id: Optional[str] = None):
        super().__init__(agent, model_id)
        self._agent.system_prompt = PromptService.get_system_prompt(AgentType.CONVERSATION_SUMMARIZER)

    def execute(self, conversation_history: List[str]) -> str:
        """
        Summarizes a conversation history into a single paragraph.
        """
        print("Executing Conversation Summarizer Agent...")
        history_str = "\n".join(conversation_history)
        user_prompt = PromptService.format_user_prompt(
            AgentType.CONVERSATION_SUMMARIZER,
            "summarize",
            history_str=history_str
        )
        result = self._agent(user_prompt)
        return str(result)  # type: ignore
