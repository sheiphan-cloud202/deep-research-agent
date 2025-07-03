from deep_research_agent.common.handlers import (
    ClarifierHandler,
    ConversationSummarizerHandler,
    DevilsAdvocateHandler,
    EvaluationCoordinatorHandler,
    IdeationHandler,
    QueryEnhancerHandler,
    QueryUnderstandingHandler,
    RankingHandler,
    ReportSynthesizerHandler,
    SearchSummarizerHandler,
)
from deep_research_agent.common.schemas import AgentType
from deep_research_agent.services.prompt_service import PromptService

# Create a single shared PromptService instance
_prompt_service = PromptService()

AGENT_REGISTRY = {
    AgentType.CLARIFIER: ClarifierHandler(prompt_service=_prompt_service),
    AgentType.CONVERSATION_SUMMARIZER: ConversationSummarizerHandler(prompt_service=_prompt_service),
    AgentType.QUERY_ENHANCER: QueryEnhancerHandler(prompt_service=_prompt_service),
    AgentType.QUERY_UNDERSTANDING: QueryUnderstandingHandler(prompt_service=_prompt_service),
    AgentType.SEARCH_SUMMARIZER: SearchSummarizerHandler(prompt_service=_prompt_service),
    AgentType.IDEATION: IdeationHandler(prompt_service=_prompt_service),
    AgentType.DEVILS_ADVOCATE: DevilsAdvocateHandler(prompt_service=_prompt_service),
    AgentType.EVALUATION_COORDINATOR: EvaluationCoordinatorHandler(prompt_service=_prompt_service),
    AgentType.RANKING: RankingHandler(prompt_service=_prompt_service),
    AgentType.REPORT_SYNTHESIZER: ReportSynthesizerHandler(prompt_service=_prompt_service),
}
