import re
from typing import Any

from deep_research_agent.agents.base_agent import BaseAgent
from deep_research_agent.common.schemas import AgentType, AwaitingUserInputError
from deep_research_agent.core.agent_factory import AgentFactory
from deep_research_agent.services.prompt_service import PromptService
from deep_research_agent.utils.logger import logger


class ClarifierAgent(BaseAgent):
    def __init__(self, prompt_service: PromptService, model_id: str | None = None):
        super().__init__(prompt_service)
        self._agent = AgentFactory.create_agent(model_id)
        if self.prompt_service:
            self._agent.system_prompt = self.prompt_service.get_system_prompt(AgentType.CLARIFIER)

    def execute(self, context: dict[str, Any]):
        if not self.prompt_service:
            raise ValueError("PromptService is not available for ClarifierAgent")

        conversation_history = context.get("conversation_history", [])
        if not conversation_history:
            logger.warning("ClarifierAgent expects 'conversation_history' in the context, but it was empty.")
            return

        trigger_words = [
            "start the agent",
            "yes",
            "run",
            "start agent",
            "begin",
            "go",
        ]
        latest_user_response = conversation_history[-1]

        # Use regex with word boundaries to avoid matching substrings within words (e.g., "go" in "governance")
        if any(
            re.search(r"\b" + re.escape(trigger) + r"\b", latest_user_response, re.IGNORECASE)
            for trigger in trigger_words
        ):
            logger.info("\n✅ Great! Moving to the next step...\n")
            return

        logger.info("\n💭 Let me ask you some clarifying questions to better understand your idea...\n")

        # Check if there are document summaries in the context
        document_summaries = context.get("document_summaries", [])

        if document_summaries:
            # Use document-aware clarifying questions
            logger.info("📄 I've analyzed your uploaded documents. Let me ask some targeted questions...\n")

            # Extract original request (before document analysis was added)
            original_request = (
                conversation_history[0].split("\n\nDocument Analysis:")[0]
                if "Document Analysis:" in conversation_history[0]
                else conversation_history[0]
            )

            # Get consolidated document summary
            document_summary = ""
            if len(document_summaries) == 1:
                document_summary = document_summaries[0]["summary"]
            else:
                # Multiple documents - create a brief overview
                document_summary = "\n\n".join(
                    [f"File: {doc['file_name']}\nSummary: {doc['summary'][:300]}..." for doc in document_summaries]
                )

            prompt = self.prompt_service.format_user_prompt(
                AgentType.CLARIFIER,
                "with_documents",
                initial_request=original_request,
                document_summary=document_summary,
            )
        else:
            # Use regular clarifying questions
            latest_context = conversation_history[-1]
            full_context = "\n".join(conversation_history)

            prompt = self.prompt_service.format_user_prompt(
                AgentType.CLARIFIER,
                "interactive",
                latest_context=latest_context,
                full_context=full_context,
            )

        clarifying_questions = self._agent(prompt)
        logger.info(f"🤔 {clarifying_questions}\n")

        raise AwaitingUserInputError(str(clarifying_questions))
