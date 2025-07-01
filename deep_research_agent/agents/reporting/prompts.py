"""
Prompts for reporting agents.
"""

from deep_research_agent.common.schemas import AgentType

# System prompts for reporting agents
SYSTEM_PROMPTS = {
    AgentType.REPORT_SYNTHESIZER: (
        "You are a Report Synthesizer Agent. Your job is to create a final, comprehensive, and well-structured "
        "report in Markdown format. The report should summarize the entire research and ideation process, "
        "highlighting the top-ranked idea, its scores, and the justification for its ranking. "
        "Use the provided creative brief and ranked list of ideas to generate the report."
    ),
}

# User prompt templates for reporting agents
USER_PROMPT_TEMPLATES = {
    AgentType.REPORT_SYNTHESIZER: {
        "synthesize": (
            "Please create a final, compelling report in Markdown format. "
            "The report should be based on the following creative brief and ranked list of ideas.\n\n"
            "## Creative Brief\n{creative_brief}\n\n"
            "## Ranked and Scored Ideas\n{ranked_list_json}\n\n"
            "The report should start with an executive summary, then detail the top-ranked idea, "
            "its scores, and a compelling justification. It should be professional and easy to read."
        )
    },
} 