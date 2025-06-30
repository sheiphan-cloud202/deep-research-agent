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
    
    # Import prompt service for consistent prompting
    from deep_research_agent.prompt_service import PromptService, AgentType
    
    # Create an agent with the websearch tool
    analysis_agent = Agent(
        model=agent.model,
        tools=[websearch],
        system_prompt=PromptService.get_system_prompt(AgentType.BUSINESS_ANALYSIS)
    )
    
    # Call the agent and return its response
    user_prompt = PromptService.format_user_prompt(
        AgentType.BUSINESS_ANALYSIS,
        "analyze",
        query=query
    )
    result = analysis_agent(user_prompt)
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
