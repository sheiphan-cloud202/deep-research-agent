import asyncio

from strands import Agent, tool

from deep_research_agent.agents.research.tools import websearch
from deep_research_agent.common.schemas import AgentType
from deep_research_agent.services.prompt_service import PromptService
from deep_research_agent.utils.logger import logger


@tool
def business_analysis(query: str, agent: Agent | None = None) -> str:
    """
    Performs business analysis on market and impact.

    Args:
        query: The analysis query
        agent: Shared Agent instance (if None, creates a new one)
    """
    logger.info(f"Executing Business Analysis with query: {query}")

    if agent is None:
        from strands.models import BedrockModel

        from deep_research_agent.common.config import settings

        model = BedrockModel(
            model_id="anthropic.claude-3-sonnet-20240229-v1:0",
            region_name=settings.aws_region,
        )
        agent = Agent(model=model)

    # Initialize prompt service to access system and user prompts
    prompt_service = PromptService()

    # Create an agent with the websearch tool and the appropriate system prompt
    analysis_agent = Agent(
        model=agent.model,
        tools=[websearch],
        system_prompt=prompt_service.get_system_prompt(AgentType.BUSINESS_ANALYSIS),
    )

    # Build the user prompt using the template
    user_prompt = prompt_service.format_user_prompt(AgentType.BUSINESS_ANALYSIS, "analyze", query=query)

    # Call the agent and return its response
    result = analysis_agent(user_prompt)
    return str(result)


async def business_analysis_async(query: str, agent: Agent | None = None) -> str:
    """
    Async version of business_analysis for parallel execution.

    Args:
        query: The analysis query
        agent: Shared Agent instance (if None, creates a new one)
    """
    # Run the synchronous function in a thread pool to avoid blocking
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, business_analysis, query, agent)
