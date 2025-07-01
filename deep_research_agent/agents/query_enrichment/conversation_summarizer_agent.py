from typing import List, Optional
from strands import Agent
from deep_research_agent.agents.base_agent import BaseAgent
from deep_research_agent.common.schemas import AgentType
from deep_research_agent.services.prompt_service import PromptService
from deep_research_agent.utils.logger import logger


class ConversationSummarizerAgent(BaseAgent):
    def __init__(self, prompt_service: PromptService, agent: Optional[Agent] = None, model_id: Optional[str] = None):
        super().__init__(agent, model_id)
        self.prompt_service = prompt_service
        self._agent.system_prompt = self.prompt_service.get_system_prompt(AgentType.CONVERSATION_SUMMARIZER)

    def execute(self, conversation_history: List[str]) -> str:
        """
        Summarizes a conversation history into a single paragraph.
        """
        logger.info("Executing Conversation Summarizer Agent...")
        history_str = "\n".join(conversation_history)
        user_prompt = self.prompt_service.format_user_prompt(
            AgentType.CONVERSATION_SUMMARIZER,
            "summarize",
            history_str=history_str
        )
        result = self._agent(user_prompt)
        return str(result)  # type: ignore
