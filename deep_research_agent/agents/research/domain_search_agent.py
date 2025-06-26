import asyncio
from strands import Agent, tool
from deep_research_agent.agents.research.tools import websearch
from typing import Optional


@tool
def domain_search(query: str, agent: Optional[Agent] = None) -> str:
    """
    Performs a domain-specific search for niche insights.
    
    Args:
        query: The search query
        agent: Shared Agent instance (if None, creates a new one)
    """
    print(f"Executing Domain Search with query: {query}")
    
    if agent is None:
        from strands.models import BedrockModel
        model = BedrockModel(
            model_id="us.anthropic.claude-3-7-sonnet-20250219-v1:0",
            region_name="us-east-1"
        )
        agent = Agent(model=model)
    
    # Create an agent with the websearch tool
    search_agent = Agent(
        model=agent.model,
        tools=[websearch],
        system_prompt=(
            "You are a Domain-Specific Search Agent. Your task is to perform a deep, targeted web search "
            "for niche, expert-level insights on a given query. You may need to look into scientific papers, "
            "clinical studies, or technical documentation. Synthesize the findings into a concise summary."
        )
    )
    
    # Call the agent and return its response
    result = search_agent(
        f"Perform a domain-specific, in-depth search for expert insights on: {query}"
    )
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
