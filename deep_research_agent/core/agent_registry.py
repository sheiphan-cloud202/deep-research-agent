from deep_research_agent.agents.evaluation.evaluation_coordinator_agent import EvaluationCoordinatorAgent
from deep_research_agent.agents.evaluation.ranking_agent import RankingAgent
from deep_research_agent.agents.ideation.devils_advocate_agent import DevilsAdvocateAgent
from deep_research_agent.agents.ideation.ideation_agent import IdeationAgent
from deep_research_agent.agents.query_enrichment.clarifier_agent import ClarifierAgent
from deep_research_agent.agents.query_enrichment.conversation_summarizer_agent import ConversationSummarizerAgent
from deep_research_agent.agents.query_enrichment.document_summarizer_agent import DocumentSummarizerAgent
from deep_research_agent.agents.query_enrichment.query_enhancer_agent import QueryEnhancerAgent
from deep_research_agent.agents.query_enrichment.query_understanding_agent import QueryUnderstandingAgent
from deep_research_agent.agents.reporting.report_synthesizer_agent import ReportSynthesizerAgent
from deep_research_agent.agents.research.parallel_research_agent import ParallelResearchAgent
from deep_research_agent.agents.research.search_summarizer_agent import SearchSummarizerAgent
from deep_research_agent.common.schemas import AgentType

AGENT_REGISTRY = {
    AgentType.DOCUMENT_SUMMARIZER: DocumentSummarizerAgent,
    AgentType.CLARIFIER: ClarifierAgent,
    AgentType.CONVERSATION_SUMMARIZER: ConversationSummarizerAgent,
    AgentType.QUERY_ENHANCER: QueryEnhancerAgent,
    AgentType.QUERY_UNDERSTANDING: QueryUnderstandingAgent,
    AgentType.PARALLEL_RESEARCH: ParallelResearchAgent,
    AgentType.SEARCH_SUMMARIZER: SearchSummarizerAgent,
    AgentType.IDEATION: IdeationAgent,
    AgentType.DEVILS_ADVOCATE: DevilsAdvocateAgent,
    AgentType.EVALUATION_COORDINATOR: EvaluationCoordinatorAgent,
    AgentType.RANKING: RankingAgent,
    AgentType.REPORT_SYNTHESIZER: ReportSynthesizerAgent,
}
