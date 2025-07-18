from enum import Enum

from pydantic import BaseModel, Field


class AgentType(str, Enum):
    # Document Processing
    DOCUMENT_SUMMARIZER = "document_summarizer"

    # Query Enrichment
    CONVERSATION_SUMMARIZER = "conversation_summarizer"
    QUERY_UNDERSTANDING = "query_understanding"
    QUERY_ENHANCER = "query_enhancer"
    CLARIFIER = "clarifier"

    # Ideation
    IDEATION = "ideation"
    DEVILS_ADVOCATE = "devils_advocate"

    # Research
    DOMAIN_SEARCH = "domain_search"
    GENERIC_SEARCH = "generic_search"
    BUSINESS_ANALYSIS = "business_analysis"
    USER_PERSONA = "user_persona"
    TREND_SPOTTER = "trend_spotter"
    SEARCH_SUMMARIZER = "search_summarizer"
    PARALLEL_RESEARCH = "parallel_research"

    # Evaluation
    TECHNICAL_FEASIBILITY = "technical_feasibility"
    MARKET_VIABILITY = "market_viability"
    ETHICAL_GUARDIAN = "ethical_guardian"
    RANKING = "ranking"
    EVALUATION_COORDINATOR = "evaluation_coordinator"

    # Reporting
    REPORT_SYNTHESIZER = "report_synthesizer"
    CITATION_REPORT_GENERATOR = "citation_report_generator"


class SearchResult(BaseModel):
    title: str
    url: str
    snippet: str
    content: str | None = None
    source: str


class TrendResult(BaseModel):
    trend_name: str
    description: str
    search_volume: str
    related_topics: list[str]


class AwaitingUserInputError(Exception):
    def __init__(self, questions: str):
        self.questions = questions
        super().__init__(questions)


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
    id: str = Field(..., description="A unique identifier for the use case.")
    title: str = Field(..., description="The title of the use case.")
    description: str = Field(..., description="A detailed description of the use case.")
    business_value: str = Field(..., description="The business value and impact of the use case.")
    technical_requirements: list[str] = Field(
        default_factory=list, description="List of technical requirements and technologies."
    )
    priority: str = Field(default="Medium", description="The priority level (e.g., Critical, High, Medium, Low).")
    complexity: str = Field(default="Medium", description="The implementation complexity (e.g., High, Medium, Low).")
    citations: list[str] = Field(default_factory=list, description="List of sources or research citations.")
    aws_services: list[str] = Field(default_factory=list, description="List of AWS services required.")
    implementation_approach: str = Field(default="", description="Implementation approach description.")
    estimated_timeline: str = Field(default="", description="Timeline estimate.")
    cost_estimate: str = Field(default="", description="Cost estimate.")
    current_implementation: str = Field(default="", description="Current implementation status.")
    proposed_solution: str = Field(default="", description="Proposed solution description.")


class UseCases(BaseModel):
    use_cases: list[UseCase] = Field(..., description="A list of use cases.")
