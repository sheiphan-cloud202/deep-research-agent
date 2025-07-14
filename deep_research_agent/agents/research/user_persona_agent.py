import asyncio

from strands import Agent, tool

from deep_research_agent.agents.research.tools import websearch
from deep_research_agent.common.schemas import AgentType, MissionBrief
from deep_research_agent.services.prompt_service import PromptService
from deep_research_agent.utils.logger import logger


@tool
def user_persona_agent(mission_brief: MissionBrief, agent: Agent | None = None) -> str:
    """
    Creates a detailed user persona based on a mission brief.

    Args:
        mission_brief: The mission brief containing the topic and industry.
        agent: Shared Agent instance (if None, creates a new one).
    """
    logger.info("Executing User Persona Agent...")

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

    # Create a user persona agent with the websearch tool
    persona_agent = Agent(
        model=agent.model,
        tools=[websearch],
        system_prompt=prompt_service.get_system_prompt(AgentType.USER_PERSONA),
    )

    # Build the user prompt using the template
    user_prompt = prompt_service.format_user_prompt(
        AgentType.USER_PERSONA,
        "create_persona",
        topic=mission_brief.main_topic,
        industry=mission_brief.industry,
    )

    # Call the agent and return its response
    result = persona_agent(user_prompt)
    return str(result)


async def user_persona_agent_async(mission_brief: MissionBrief, agent: Agent | None = None) -> str:
    """
    Async version of user_persona_agent for parallel execution.

    Args:
        mission_brief: The mission brief containing the topic and industry.
        agent: Shared Agent instance (if None, creates a new one).
    """
    # Run the synchronous function in a thread pool to avoid blocking
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, user_persona_agent, mission_brief, agent)
