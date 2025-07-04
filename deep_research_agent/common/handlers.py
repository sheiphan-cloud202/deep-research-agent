from abc import ABC, abstractmethod
from typing import Any, cast

from deep_research_agent.agents.evaluation.evaluation_coordinator_agent import EvaluationCoordinatorAgent
from deep_research_agent.agents.evaluation.ranking_agent import RankingAgent
from deep_research_agent.agents.ideation.devils_advocate_agent import DevilsAdvocateAgent
from deep_research_agent.agents.ideation.ideation_agent import IdeationAgent
from deep_research_agent.agents.query_enrichment.clarifier_agent import ClarifierAgent
from deep_research_agent.agents.query_enrichment.conversation_summarizer_agent import ConversationSummarizerAgent
from deep_research_agent.agents.query_enrichment.query_enhancer_agent import QueryEnhancerAgent
from deep_research_agent.agents.query_enrichment.query_understanding_agent import QueryUnderstandingAgent
from deep_research_agent.agents.reporting.report_synthesizer_agent import ReportSynthesizerAgent
from deep_research_agent.agents.research.search_summarizer_agent import SearchSummarizerAgent
from deep_research_agent.common.config import settings
from deep_research_agent.common.schemas import UseCases
from deep_research_agent.services.prompt_service import PromptService
from deep_research_agent.utils.logger import logger


class WorkflowStepHandler(ABC):
    """Abstract base class for a workflow step handler."""

    def __init__(self, prompt_service: PromptService):
        self.prompt_service = prompt_service

    @abstractmethod
    def execute(self, context: dict[str, Any]) -> None:
        """Execute the workflow step."""
        pass

    def _get_agent_class(self):
        # To be implemented by subclasses that need it
        raise NotImplementedError

    def _get_prompt_service(self):
        # To be implemented by subclasses that need it
        raise NotImplementedError


class ClarifierHandler(WorkflowStepHandler):
    def execute(self, context: dict[str, Any]):
        agent = ClarifierAgent(prompt_service=self.prompt_service)
        conversation_history = context.get("conversation_history", [])
        if not conversation_history:
            logger.warning("ClarifierHandler expects 'conversation_history' in the context, but it was empty.")
            return

        trigger_words = ["start the agent", "yes", "run", "start agent", "begin", "go"]
        logger.info("\n💭 Let me ask you some clarifying questions to better understand your idea...\n")

        while True:
            # Use the latest entry in conversation history for context
            latest_context = conversation_history[-1] if conversation_history else ""
            full_context = "\n".join(conversation_history)

            # Generate questions
            clarifying_questions = agent.execute_interactive(latest_context, full_context)
            logger.info(f"🤔 {clarifying_questions}\n")

            # Get user response
            user_response = input("Your response (or say 'start the agent'/'yes'/'run' when ready): ").strip()

            if not user_response:
                logger.warning("Please provide a response or say when you're ready to start.\n")
                continue

            # Add response to conversation history before checking for trigger words
            conversation_history.append(user_response)

            # Check for trigger words
            if any(trigger.lower() in user_response.lower() for trigger in trigger_words):
                logger.info("\n✅ Great! Moving to the next step...\n")
                break

            logger.info("")  # Add spacing for readability

        # Update the context with the full conversation
        context["conversation_history"] = conversation_history


class ConversationSummarizerHandler(WorkflowStepHandler):
    def execute(self, context: dict[str, Any]):
        agent = ConversationSummarizerAgent(prompt_service=self.prompt_service)
        result = agent.execute(context["conversation_history"])
        context["summary"] = result
        logger.info(f"Conversation Summary:\n{result}\n")


class QueryEnhancerHandler(WorkflowStepHandler):
    def execute(self, context: dict[str, Any]):
        agent = QueryEnhancerAgent(prompt_service=self.prompt_service)
        result = agent.execute(context["summary"])
        context["enhanced_prompt"] = result
        logger.info(f"Enhanced Prompt:\n{result}\n")


class QueryUnderstandingHandler(WorkflowStepHandler):
    def execute(self, context: dict[str, Any]):
        agent = QueryUnderstandingAgent(prompt_service=self.prompt_service, model_id=settings.claude_sonnet_model_id)
        result = agent.execute(context["enhanced_prompt"])
        context["mission_brief"] = result
        logger.info(f"Mission Brief:\n{result.model_dump_json(indent=2)}\n")


class SearchSummarizerHandler(WorkflowStepHandler):
    def execute(self, context: dict[str, Any]):
        agent = SearchSummarizerAgent(prompt_service=self.prompt_service)
        result = agent.execute(context["research_results"])
        context["creative_brief"] = result
        logger.info(f"Creative Brief:\n{result}\n")


class IdeationHandler(WorkflowStepHandler):
    def execute(self, context: dict[str, Any]):
        agent = IdeationAgent(prompt_service=self.prompt_service)
        creative_brief = context["creative_brief"]
        feedback = context.get("devils_advocate_feedback")
        if feedback:
            result = agent.execute(creative_brief, feedback=feedback)
            context["refined_ideas"] = result
            logger.info(f"Refined Ideas:\n{result}\n")
        else:
            result = agent.execute(creative_brief)
            context["initial_ideas"] = result
            logger.info(f"Initial Ideas:\n{result}\n")


class DevilsAdvocateHandler(WorkflowStepHandler):
    def execute(self, context: dict[str, Any]):
        agent = DevilsAdvocateAgent(prompt_service=self.prompt_service)
        initial_ideas = cast(UseCases, context["initial_ideas"])
        idea_list = [f"{i.name}: {i.description}" for i in initial_ideas.use_cases]
        result = agent.execute(idea_list)
        context["devils_advocate_feedback"] = result
        logger.info(f"Devil's Advocate Feedback:\n{result}\n")


class EvaluationCoordinatorHandler(WorkflowStepHandler):
    def execute(self, context: dict[str, Any]):
        agent = EvaluationCoordinatorAgent(prompt_service=self.prompt_service)
        refined_ideas = cast(UseCases, context["refined_ideas"])
        idea_list = [f"{i.name}: {i.description}" for i in refined_ideas.use_cases]
        result = agent.execute(idea_list)
        context["scored_ideas"] = result


class RankingHandler(WorkflowStepHandler):
    def __init__(self, prompt_service: PromptService):
        super().__init__(prompt_service)
        # RankingAgent doesn't need prompt_service, but we keep the consistent interface

    def execute(self, context: dict[str, Any]):
        agent = RankingAgent()
        result = agent.execute(context["scored_ideas"])
        context["ranked_ideas"] = result
        logger.info(f"Ranked Ideas:\n{result}\n")


class ReportSynthesizerHandler(WorkflowStepHandler):
    def execute(self, context: dict[str, Any]):
        agent = ReportSynthesizerAgent(prompt_service=self.prompt_service)
        result = agent.execute(context["ranked_ideas"], context["creative_brief"])
        context["final_report"] = result
