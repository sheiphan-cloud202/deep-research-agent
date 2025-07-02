import asyncio

from strands import Agent, tool

from deep_research_agent.agents.research.tools import websearch
from deep_research_agent.common.schemas import MissionBrief


@tool
def user_persona_agent(mission: MissionBrief, agent: Agent | None = None) -> str:
    """
    Creates detailed user personas based on the mission brief.

    Args:
        mission: The mission brief containing topic information
        agent: Shared Agent instance (if None, creates a new one)
    """
    print("Executing User Persona Agent...")

    if agent is None:
        from strands.models import BedrockModel

        model = BedrockModel(
            model_id="us.anthropic.claude-3-7-sonnet-20250219-v1:0",
            region_name="us-east-1",
        )
        agent = Agent(model=model)

    # Import prompt service for consistent prompting
    from deep_research_agent.common.schemas import AgentType
    from deep_research_agent.services.prompt_service import PromptService

    # Initialize the prompt service to fetch system and user prompts
    prompt_service = PromptService()

    # Create an agent with the websearch tool and the appropriate system prompt
    persona_agent = Agent(
        model=agent.model,
        tools=[websearch],
        system_prompt=prompt_service.get_system_prompt(AgentType.USER_PERSONA),
    )

    # Build the user prompt from the template
    user_prompt = prompt_service.format_user_prompt(
        AgentType.USER_PERSONA,
        "create_persona",
        user_data=f"Mission: {mission.main_topic}",
    )
    result = persona_agent(user_prompt)
    return str(result)


async def user_persona_agent_async(mission: MissionBrief, agent: Agent | None = None) -> str:
    """
    Async version of user_persona_agent for parallel execution.

    Args:
        mission: The mission brief containing topic information
        agent: Shared Agent instance (if None, creates a new one)
    """
    # Run the synchronous function in a thread pool to avoid blocking
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, user_persona_agent, mission, agent)
