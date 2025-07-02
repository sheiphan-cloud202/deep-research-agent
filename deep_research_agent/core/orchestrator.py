import asyncio

from deep_research_agent.agents.query_enrichment.clarifier_agent import ClarifierAgent
from deep_research_agent.agents.research.business_analysis_agent import business_analysis_async
from deep_research_agent.agents.research.domain_search_agent import domain_search_async
from deep_research_agent.agents.research.generic_search_agent import generic_search_async
from deep_research_agent.agents.research.trend_spotter_agent import trend_spotter_async
from deep_research_agent.agents.research.user_persona_agent import user_persona_agent_async
from deep_research_agent.common.schemas import AgentType, MissionBrief
from deep_research_agent.core.agent_factory import AgentFactory
from deep_research_agent.core.agent_registry import AGENT_REGISTRY, _prompt_service
from deep_research_agent.core.workflow import DEFAULT_WORKFLOW, PARALLEL_RESEARCH_STEP
from deep_research_agent.utils.logger import logger


class OrchestratorAgent:
    def __init__(self, workflow: list | None = None):
        self._agent = AgentFactory.get_default_agent()
        self.workflow_context = {}  # Stores the outputs of each step
        self.workflow = workflow if workflow else DEFAULT_WORKFLOW

    def generate_clarifying_questions(self, conversation_history: list) -> str:
        """
        Generate clarifying questions based on the conversation history.
        """
        clarifier_agent = ClarifierAgent(prompt_service=_prompt_service)

        # Use the latest entry in conversation history for context
        latest_context = conversation_history[-1] if conversation_history else ""
        full_context = " ".join(conversation_history)

        return clarifier_agent.execute_interactive(latest_context, full_context)

    def run_workflow_from_conversation(self, conversation_history: list):
        """
        Run the complete, dynamically configured workflow using conversation history.
        """
        self.workflow_context = {"conversation_history": conversation_history}

        for step in self.workflow:
            if step == PARALLEL_RESEARCH_STEP:
                self._execute_parallel_research()
            else:
                self._execute_step(step)

        final_report = self.workflow_context.get(
            "final_report", "Workflow finished, but no final report was generated."
        )
        logger.info("\n--- END OF WORKFLOW ---")
        logger.info(f"Final Report:\n{final_report}")
        return final_report

    def _execute_step(self, agent_type: AgentType):
        logger.info(f"--- Executing Step: {agent_type.value} ---")
        handler = AGENT_REGISTRY.get(agent_type)
        if not handler:
            raise ValueError(f"No handler found for agent type: {agent_type.value}")

        handler.execute(self.workflow_context)

    def _execute_parallel_research(self):
        logger.info("--- Executing Step: Parallel Research ---")
        mission_brief = self.workflow_context.get("mission_brief")
        assert isinstance(mission_brief, MissionBrief), "Mission brief must be of type MissionBrief"

        research_results = asyncio.run(self.run_research_agents_parallel(mission_brief))
        self.workflow_context["research_results"] = research_results

    async def run_research_agents_parallel(self, mission_brief: MissionBrief):
        """
        Run all research agents in parallel for faster execution.
        """
        logger.info("Starting parallel research phase...")
        research_tasks = [
            generic_search_async(mission_brief.decomposed_tasks.generic_search_query, self._agent),
            business_analysis_async(mission_brief.decomposed_tasks.business_analysis_query, self._agent),
            domain_search_async(mission_brief.decomposed_tasks.domain_specific_query, self._agent),
            trend_spotter_async(mission_brief.decomposed_tasks.trend_spotter_query, self._agent),
            user_persona_agent_async(mission_brief, self._agent),
        ]

        research_results = await asyncio.gather(*research_tasks, return_exceptions=True)

        processed_results, agent_names = (
            [],
            [
                "Generic Search",
                "Business Analysis",
                "Domain Search",
                "Trend Spotter",
                "User Persona",
            ],
        )
        for i, result in enumerate(research_results):
            if isinstance(result, Exception):
                logger.warning(f"Warning: {agent_names[i]} agent failed with error: {result}")
                processed_results.append(f"Error in {agent_names[i]}: {str(result)}")
            else:
                processed_results.append(str(result))

        logger.info("Parallel research phase completed!")
        return processed_results
