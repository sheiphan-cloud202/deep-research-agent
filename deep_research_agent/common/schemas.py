from enum import Enum

from pydantic import BaseModel, Field


class AgentType(Enum):
    """Enumeration of all agent types in the system"""

    # Evaluation agents
    ETHICAL_GUARDIAN = "ethical_guardian"
    EVALUATION_COORDINATOR = "evaluation_coordinator"
    MARKET_VIABILITY = "market_viability"
    RANKING = "ranking"
    TECHNICAL_FEASIBILITY = "technical_feasibility"

    # Ideation agents
    DEVILS_ADVOCATE = "devils_advocate"
    IDEATION = "ideation"

    # Query enrichment agents
    CLARIFIER = "clarifier"
    CONVERSATION_SUMMARIZER = "conversation_summarizer"
    QUERY_ENHANCER = "query_enhancer"
    QUERY_UNDERSTANDING = "query_understanding"

    # Reporting agents
    REPORT_SYNTHESIZER = "report_synthesizer"

    # Research agents
    BUSINESS_ANALYSIS = "business_analysis"
    DOMAIN_SEARCH = "domain_search"
    GENERIC_SEARCH = "generic_search"
    SEARCH_SUMMARIZER = "search_summarizer"
    TREND_SPOTTER = "trend_spotter"
    USER_PERSONA = "user_persona"
    PARALLEL_RESEARCH = "parallel_research"


class Filters(BaseModel):
    include: list[str] = Field(..., description="List of keywords to include.")
    exclude: list[str] = Field(..., description="List of keywords to exclude.")


class DecomposedTasks(BaseModel):
    generic_search_query: str
    business_analysis_query: str
    domain_specific_query: str
    trend_spotter_query: str


class MissionBrief(BaseModel):
    main_topic: str = Field(..., description="The main topic of the research.")
    industry: str = Field(..., description="The target industry for the research.")
    tools_and_tech: list[str] = Field(..., description="Relevant tools and technologies.")
    filters: Filters = Field(..., description="Inclusion and exclusion criteria.")
    decomposed_tasks: DecomposedTasks = Field(..., description="Specific queries for research agents.")


class EvaluationScore(BaseModel):
    agent: str = Field(..., description="The name of the agent providing the score.")
    score: int = Field(..., ge=1, le=10, description="The score from 1 to 10.")
    justification: str = Field(..., description="The justification for the score.")


class UseCase(BaseModel):
    name: str = Field(..., description="The name of the use case.")
    description: str = Field(..., description="A detailed description of the use case.")
    area: str = Field(..., description="The business area or department it belongs to.")
    category: str = Field(
        ...,
        description="The category of the use case (e.g., Customer Service, Operations).",
    )
    priority: int = Field(..., ge=1, le=5, description="The priority of the use case (1-5).")
    impact_score: int = Field(..., ge=1, le=10, description="The potential impact of the use case (1-10).")
    implementation_complexity: str = Field(..., description="The complexity of implementing the use case.")
    alignment_score: int = Field(
        ...,
        ge=1,
        le=10,
        description="How well the use case aligns with business goals (1-10).",
    )
    business_value: str = Field(..., description="The business value proposition.")
    estimated_roi: str = Field(..., description="The estimated return on investment.")
    key_benefits: list[str] = Field(..., description="A list of key benefits.")
    success_metrics: list[str] = Field(..., description="Metrics to measure success.")
    prerequisites: list[str] = Field(..., description="Prerequisites for implementation.")
    estimated_timeline: str = Field(..., description="An estimated timeline for implementation.")
    risk_factors: list[str] = Field(..., description="Potential risks and mitigation strategies.")
    technologies_used: list[str] = Field(..., description="A list of technologies required.")


class UseCases(BaseModel):
    use_cases: list[UseCase] = Field(..., description="A list of use cases.")
