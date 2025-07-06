import asyncio
from typing import Any

from deep_research_agent.agents.base_agent import BaseAgent
from deep_research_agent.agents.research.business_analysis_agent import business_analysis_async
from deep_research_agent.agents.research.domain_search_agent import domain_search_async
from deep_research_agent.agents.research.generic_search_agent import generic_search_async
from deep_research_agent.agents.research.trend_spotter_agent import trend_spotter_async
from deep_research_agent.agents.research.user_persona_agent import user_persona_agent_async
from deep_research_agent.common.schemas import MissionBrief
from deep_research_agent.core.agent_factory import AgentFactory
from deep_research_agent.utils.logger import logger


class ParallelResearchAgent(BaseAgent):
    def __init__(self, *args, **kwargs):
        # This agent orchestrates other async functions and doesn't need its own prompt service or model
        super().__init__()

    def execute(self, context: dict[str, Any]):
        logger.info("--- Executing Step: Parallel Research ---")
        mission_brief = context.get("mission_brief")
        if not isinstance(mission_brief, MissionBrief):
            raise TypeError("Mission brief must be of type MissionBrief")

        research_results = asyncio.run(self._run_research_agents_parallel(mission_brief))
        context["research_results"] = research_results

    async def _run_research_agents_parallel(self, mission_brief: MissionBrief):
        """
        Run all research agents in parallel for faster execution.
        """
        logger.info("Starting parallel research phase...")
        shared_agent = AgentFactory.get_default_agent()
        research_tasks = [
            generic_search_async(mission_brief.decomposed_tasks.generic_search_query, shared_agent),
            business_analysis_async(mission_brief.decomposed_tasks.business_analysis_query, shared_agent),
            domain_search_async(mission_brief.decomposed_tasks.domain_specific_query, shared_agent),
            trend_spotter_async(mission_brief.decomposed_tasks.trend_spotter_query, shared_agent),
            user_persona_agent_async(mission_brief, shared_agent),
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
