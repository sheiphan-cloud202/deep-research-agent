from deep_research_agent.common.schemas import AgentType

# Define the default workflow by listing the agent types in execution order
DEFAULT_WORKFLOW = [
    AgentType.DOCUMENT_SUMMARIZER,
    AgentType.CLARIFIER,
    AgentType.CONVERSATION_SUMMARIZER,
    AgentType.QUERY_ENHANCER,
    AgentType.QUERY_UNDERSTANDING,
    AgentType.PARALLEL_RESEARCH,  # This special step runs all research agents concurrently
    AgentType.SEARCH_SUMMARIZER,
    AgentType.IDEATION,  # Generate use case ideas
    AgentType.CITATION_REPORT_GENERATOR,  # Generate comprehensive reports with citations
    # AgentType.DEVILS_ADVOCATE,
    # AgentType.IDEATION,  # Second pass for refining ideas with feedback
    # AgentType.EVALUATION_COORDINATOR,
    # AgentType.RANKING,
    # AgentType.REPORT_SYNTHESIZER,
]

# Example of a simpler workflow that could be used for different purposes
SIMPLE_WORKFLOW = [
    AgentType.DOCUMENT_SUMMARIZER,
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

# Step metadata for better progress tracking and user display
WORKFLOW_STEP_METADATA = {
    AgentType.DOCUMENT_SUMMARIZER: {
        "name": "Document Analysis",
        "description": "Analyzing uploaded documents and extracting key information",
        "estimated_duration": "30-60 seconds",
        "outputs": ["document_summaries", "key_insights"],
    },
    AgentType.CLARIFIER: {
        "name": "Query Clarification",
        "description": "Asking clarifying questions to better understand the research objectives",
        "estimated_duration": "5-10 seconds",
        "outputs": ["clarifying_questions"],
        "user_interaction": True,
    },
    AgentType.CONVERSATION_SUMMARIZER: {
        "name": "Context Summarization",
        "description": "Summarizing conversation context and user inputs",
        "estimated_duration": "10-20 seconds",
        "outputs": ["conversation_summary", "key_requirements"],
    },
    AgentType.QUERY_ENHANCER: {
        "name": "Query Enhancement",
        "description": "Enhancing and expanding search queries for better research coverage",
        "estimated_duration": "15-30 seconds",
        "outputs": ["enhanced_queries", "search_terms"],
    },
    AgentType.QUERY_UNDERSTANDING: {
        "name": "Query Analysis",
        "description": "Analyzing and understanding the research intent and scope",
        "estimated_duration": "10-20 seconds",
        "outputs": ["query_analysis", "research_scope"],
    },
    AgentType.PARALLEL_RESEARCH: {
        "name": "Multi-Agent Research",
        "description": "Running parallel research agents to gather comprehensive data",
        "estimated_duration": "2-5 minutes",
        "outputs": ["research_results", "data_collection"],
        "concurrent": True,
    },
    AgentType.SEARCH_SUMMARIZER: {
        "name": "Research Synthesis",
        "description": "Synthesizing and summarizing research findings",
        "estimated_duration": "30-60 seconds",
        "outputs": ["research_summary", "key_findings"],
    },
    AgentType.IDEATION: {
        "name": "Use Case Generation",
        "description": "Generating innovative use cases and opportunities",
        "estimated_duration": "45-90 seconds",
        "outputs": ["use_cases", "opportunities"],
    },
    AgentType.DEVILS_ADVOCATE: {
        "name": "Critical Analysis",
        "description": "Applying critical thinking and identifying potential challenges",
        "estimated_duration": "30-60 seconds",
        "outputs": ["critical_feedback", "challenges"],
    },
    AgentType.EVALUATION_COORDINATOR: {
        "name": "Evaluation Coordination",
        "description": "Coordinating evaluation of generated use cases",
        "estimated_duration": "45-90 seconds",
        "outputs": ["evaluation_results", "scores"],
    },
    AgentType.RANKING: {
        "name": "Ranking & Prioritization",
        "description": "Ranking and prioritizing use cases based on multiple criteria",
        "estimated_duration": "30-45 seconds",
        "outputs": ["ranked_use_cases", "priority_scores"],
    },
    AgentType.REPORT_SYNTHESIZER: {
        "name": "Report Generation",
        "description": "Generating comprehensive final report with recommendations",
        "estimated_duration": "60-120 seconds",
        "outputs": ["final_report", "recommendations"],
    },
    AgentType.CITATION_REPORT_GENERATOR: {
        "name": "PDF Strategy Report with Citations",
        "description": "Generating a single comprehensive PDF business strategy report with clickable citation links, consolidating all use cases by implementation stages",
        "estimated_duration": "2-3 minutes",
        "outputs": ["citation_report", "pdf_report_with_clickable_links", "staged_roadmap", "upload_urls"],
    },
}


def get_workflow_metadata(workflow: list | None = None) -> list:
    """
    Get metadata for all steps in a workflow.

    Args:
        workflow: List of AgentType steps. Defaults to DEFAULT_WORKFLOW.

    Returns:
        List of step metadata dictionaries with enhanced information.
    """
    if workflow is None:
        workflow = DEFAULT_WORKFLOW

    workflow_meta = []
    for i, agent_type in enumerate(workflow):
        step_meta = WORKFLOW_STEP_METADATA.get(
            agent_type,
            {
                "name": agent_type.value.replace("_", " ").title(),
                "description": f"Executing {agent_type.value} agent",
                "estimated_duration": "Unknown",
                "outputs": [],
            },
        )

        workflow_meta.append({"step_number": i, "agent_type": agent_type.value, **step_meta})

    return workflow_meta
