from deep_research_agent.common.schemas import AgentType

# Define the default workflow by listing the agent types in execution order
DEFAULT_WORKFLOW = [
    AgentType.CLARIFIER,
    AgentType.CONVERSATION_SUMMARIZER,
    AgentType.QUERY_ENHANCER,
    AgentType.QUERY_UNDERSTANDING,
    AgentType.PARALLEL_RESEARCH,  # This special step runs all research agents concurrently
    AgentType.SEARCH_SUMMARIZER,
    AgentType.IDEATION,  # First pass for initial ideas
    # AgentType.DEVILS_ADVOCATE,
    # AgentType.IDEATION,  # Second pass for refining ideas with feedback
    AgentType.EVALUATION_COORDINATOR,
    AgentType.RANKING,
    AgentType.REPORT_SYNTHESIZER,
]

# Example of a simpler workflow that could be used for different purposes
SIMPLE_WORKFLOW = [
    AgentType.CLARIFIER,
    AgentType.CONVERSATION_SUMMARIZER,
    AgentType.QUERY_ENHANCER,
    AgentType.QUERY_UNDERSTANDING,
    AgentType.PARALLEL_RESEARCH,
    AgentType.SEARCH_SUMMARIZER,
    AgentType.IDEATION,
    AgentType.RANKING,
    AgentType.REPORT_SYNTHESIZER,
]
