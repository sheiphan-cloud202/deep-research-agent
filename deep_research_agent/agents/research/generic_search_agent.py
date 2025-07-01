import asyncio
from strands import Agent, tool
from deep_research_agent.agents.research.tools import websearch
from typing import Optional
from deep_research_agent.utils.logger import logger
from deep_research_agent.common.schemas import AgentType
from deep_research_agent.services.prompt_service import PromptService


@tool
def generic_search(query: str, agent: Optional[Agent] = None) -> str:
    """
    Performs a generic search for foundational knowledge.
    
    Args:
        query: The search query
        agent: Shared Agent instance (if None, creates a new one)
    """
    logger.info(f"Executing Generic Search with query: {query}")
    
    if agent is None:
        from strands.models import BedrockModel
        model = BedrockModel(
            model_id="us.anthropic.claude-3-7-sonnet-20250219-v1:0",
            region_name="us-east-1"
        )
        agent = Agent(model=model)
    
    # Initialize prompt service to access system and user prompts
    prompt_service = PromptService()

    # Create a search agent with the websearch tool and the appropriate system prompt
    search_agent = Agent(
        model=agent.model,
        tools=[websearch],
        system_prompt=prompt_service.get_system_prompt(AgentType.GENERIC_SEARCH)
    )

    # Build the user prompt using the template
    user_prompt = prompt_service.format_user_prompt(
        AgentType.GENERIC_SEARCH,
        "search",
        topic=query
    )

    # Call the agent and return its response
    result = search_agent(user_prompt)
    return str(result)


async def generic_search_async(query: str, agent: Optional[Agent] = None) -> str:
    """
    Async version of generic_search for parallel execution.
    
    Args:
        query: The search query
        agent: Shared Agent instance (if None, creates a new one)
    """
    # Run the synchronous function in a thread pool to avoid blocking
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, generic_search, query, agent)
