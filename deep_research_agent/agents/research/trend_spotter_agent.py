import asyncio
from strands import Agent, tool
from deep_research_agent.agents.research.tools import websearch
from typing import Optional


@tool
def trend_spotter(query: str, agent: Optional[Agent] = None) -> str:
    """
    Spots future and emerging tech trends.
    
    Args:
        query: The search query
        agent: Shared Agent instance (if None, creates a new one)
    """
    print(f"Executing Trend Spotter with query: {query}")
    
    if agent is None:
        from strands.models import BedrockModel
        model = BedrockModel(
            model_id="us.anthropic.claude-3-7-sonnet-20250219-v1:0",
            region_name="us-east-1"
        )
        agent = Agent(model=model)
    
    # Create an agent with the websearch tool
    spotter_agent = Agent(
        model=agent.model,
        tools=[websearch],
        system_prompt=(
            "You are a Trend Spotter Agent. Your job is to identify future and emerging trends related to a given topic. "
            "Look for information on new technologies, market shifts, and innovative business models. "
            "Provide a summary of the key trends."
        )
    )
    
    # Call the agent and return its response
    result = spotter_agent(f"Identify emerging trends and future technologies related to: {query}")
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
