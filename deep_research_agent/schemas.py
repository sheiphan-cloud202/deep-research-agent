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
