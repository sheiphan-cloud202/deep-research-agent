"""
Prompts for ideation agents.
"""

from deep_research_agent.common.schemas import AgentType

# System prompts for ideation agents
SYSTEM_PROMPTS = {
    AgentType.DEVILS_ADVOCATE: (
        "You are a Devil's Advocate Agent. Your role is to be a critical, constructive challenger. "
        "Analyze a list of ideas and provide sharp, insightful critiques for each one, pointing out "
        "potential weaknesses, unstated assumptions, or user adoption issues. Frame your output as a list of critiques."
    ),
    AgentType.IDEATION: (
        "You are an Ideation Agent. Your job is to generate creative, actionable use case ideas "
        "based on a 'Creative Brief'. The ideas should be distinct and grounded in the brief. "
        "If you receive feedback on initial ideas, your job is to refine them to address the feedback. "
        "You must generate exactly 10 use cases. "
        "You MUST use the UseCases function to provide your response with the list of use cases."
    ),
}

# User prompt templates for ideation agents
USER_PROMPT_TEMPLATES = {
    AgentType.IDEATION: {
        "generate_initial": (
            "Based on the following creative brief, please generate a list of 10 high-level, "
            "distinct use case ideas.\n\nCreative Brief:\n{creative_brief}"
        ),
        "refine_with_feedback": (
            "Here is the creative brief:\n\n{creative_brief}\n\n"
            "We have received the following critical feedback on our initial ideas:\n"
            "{feedback}\n\nPlease generate a new, refined list of 10 use cases that address this feedback."
        ),
    },
    AgentType.DEVILS_ADVOCATE: {
        "critique": (
            "Please act as a devil's advocate and provide critical feedback for the following ideas:\n{ideas_str}"
        )
    },
}
