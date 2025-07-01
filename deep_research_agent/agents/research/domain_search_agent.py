import asyncio
from strands import Agent, tool
from deep_research_agent.agents.research.tools import websearch
from typing import Optional
from deep_research_agent.utils.logger import logger
from deep_research_agent.common.schemas import AgentType
from deep_research_agent.services.prompt_service import PromptService


@tool
def domain_search(query: str, agent: Optional[Agent] = None) -> str:
    """
    Performs a domain-specific search for niche insights.
    
    Args:
        query: The search query
        agent: Shared Agent instance (if None, creates a new one)
    """
    logger.info(f"Executing Domain Search with query: {query}")
    
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
    search_agent = Agent(
        model=agent.model,
        tools=[websearch],
        system_prompt=prompt_service.get_system_prompt(AgentType.DOMAIN_SEARCH)
    )

    # Build the user prompt using the template. Since domain information isn't provided separately,
    # we pass an empty string for the "domain" placeholder.
    user_prompt = prompt_service.format_user_prompt(
        AgentType.DOMAIN_SEARCH,
        "domain_search",
        domain="",
        query=query
    )

    # Call the agent and return its response
    result = search_agent(user_prompt)
    return str(result)


async def domain_search_async(query: str, agent: Optional[Agent] = None) -> str:
    """
    Async version of domain_search for parallel execution.
    
    Args:
        query: The search query
        agent: Shared Agent instance (if None, creates a new one)
    """
    # Run the synchronous function in a thread pool to avoid blocking
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, domain_search, query, agent)
