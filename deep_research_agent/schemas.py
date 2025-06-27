from typing import List, Dict
from pydantic import BaseModel, Field


class Filters(BaseModel):
    include: List[str] = Field(..., description="List of keywords to include.")
    exclude: List[str] = Field(..., description="List of keywords to exclude.")


class DecomposedTasks(BaseModel):
    generic_search_query: str
    business_analysis_query: str
    domain_specific_query: str
    trend_spotter_query: str


class MissionBrief(BaseModel):
    main_topic: str = Field(..., description="The main topic of the research.")
    industry: str = Field(..., description="The target industry for the research.")
    tools_and_tech: List[str] = Field(..., description="Relevant tools and technologies.")
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
    category: str = Field(..., description="The category of the use case (e.g., Customer Service, Operations).")
    priority: int = Field(..., ge=1, le=5, description="The priority of the use case (1-5).")
    impact_score: int = Field(..., ge=1, le=10, description="The potential impact of the use case (1-10).")
    implementation_complexity: str = Field(..., description="The complexity of implementing the use case.")
    alignment_score: int = Field(..., ge=1, le=10, description="How well the use case aligns with business goals (1-10).")
    business_value: str = Field(..., description="The business value proposition.")
    estimated_roi: str = Field(..., description="The estimated return on investment.")
    key_benefits: List[str] = Field(..., description="A list of key benefits.")
    success_metrics: List[str] = Field(..., description="Metrics to measure success.")
    prerequisites: List[str] = Field(..., description="Prerequisites for implementation.")
    estimated_timeline: str = Field(..., description="An estimated timeline for implementation.")
    risk_factors: List[str] = Field(..., description="Potential risks and mitigation strategies.")
    technologies_used: List[str] = Field(..., description="A list of technologies required.")


class UseCases(BaseModel):
    use_cases: List[UseCase] = Field(..., description="A list of use cases.")
