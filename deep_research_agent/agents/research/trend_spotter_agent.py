import asyncio
from strands import Agent, tool
from deep_research_agent.agents.research.tools import websearch
from typing import Optional
from deep_research_agent.utils.logger import logger
from deep_research_agent.common.schemas import AgentType
from deep_research_agent.services.prompt_service import PromptService


@tool
def trend_spotter(query: str, agent: Optional[Agent] = None) -> str:
    """
    Spots future and emerging tech trends.
    
    Args:
        query: The search query
        agent: Shared Agent instance (if None, creates a new one)
    """
    logger.info(f"Executing Trend Spotter with query: {query}")
    
    if agent is None:
        from strands.models import BedrockModel
        model = BedrockModel(
            model_id="us.anthropic.claude-3-7-sonnet-20250219-v1:0",
            region_name="us-east-1"
        )
        agent = Agent(model=model)
    
    # Initialize prompt service to access system and user prompts
    prompt_service = PromptService()

    # Create an agent with the websearch tool and the appropriate system prompt
    spotter_agent = Agent(
        model=agent.model,
        tools=[websearch],
        system_prompt=prompt_service.get_system_prompt(AgentType.TREND_SPOTTER)
    )

    # Build the user prompt using the template, mapping the query to the expected 'data' placeholder
    user_prompt = prompt_service.format_user_prompt(
        AgentType.TREND_SPOTTER,
        "identify_trends",
        data=query
    )

    # Call the agent and return its response
    result = spotter_agent(user_prompt)
    return str(result)


async def trend_spotter_async(query: str, agent: Optional[Agent] = None) -> str:
    """
    Async version of trend_spotter for parallel execution.
    
    Args:
        query: The search query
        agent: Shared Agent instance (if None, creates a new one)
    """
    # Run the synchronous function in a thread pool to avoid blocking
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, trend_spotter, query, agent)
