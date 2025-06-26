import asyncio
from strands import Agent, tool
from deep_research_agent.agents.research.tools import websearch
from typing import Optional


@tool
def business_analysis(query: str, agent: Optional[Agent] = None) -> str:
    """
    Performs business analysis on market and impact.
    
    Args:
        query: The analysis query
        agent: Shared Agent instance (if None, creates a new one)
    """
    print(f"Executing Business Analysis with query: {query}")
    
    if agent is None:
        from strands.models import BedrockModel
        model = BedrockModel(
            model_id="us.anthropic.claude-3-7-sonnet-20250219-v1:0",
            region_name="us-east-1"
        )
        agent = Agent(model=model)
    
    # Create an agent with the websearch tool
    analysis_agent = Agent(
        model=agent.model,
        tools=[websearch],
        system_prompt=(
            "You are a Business Analysis Agent. Your task is to perform a web search based on a given query "
            "to analyze the market size, economic impact, and business potential of a topic. "
            "Synthesize the findings into a concise report."
        )
    )
    
    # Call the agent and return its response
    result = analysis_agent(
        f"Perform a business analysis and market research on the following topic: {query}"
    )
    return str(result)


async def business_analysis_async(query: str, agent: Optional[Agent] = None) -> str:
    """
    Async version of business_analysis for parallel execution.
    
    Args:
        query: The analysis query
        agent: Shared Agent instance (if None, creates a new one)
    """
    # Run the synchronous function in a thread pool to avoid blocking
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, business_analysis, query, agent)
