import asyncio
from strands import Agent
from strands.models import BedrockModel
from deep_research_agent.schemas import MissionBrief
from deep_research_agent.agents.query_enrichment.clarifier_agent import ClarifierAgent
from deep_research_agent.agents.query_enrichment.conversation_summarizer_agent import ConversationSummarizerAgent
from deep_research_agent.agents.query_enrichment.query_enhancer_agent import QueryEnhancerAgent
from deep_research_agent.agents.query_enrichment.query_understanding_agent import QueryUnderstandingAgent
from deep_research_agent.agents.research.generic_search_agent import generic_search, generic_search_async
from deep_research_agent.agents.research.business_analysis_agent import business_analysis, business_analysis_async
from deep_research_agent.agents.research.domain_search_agent import domain_search, domain_search_async
from deep_research_agent.agents.research.trend_spotter_agent import trend_spotter, trend_spotter_async
from deep_research_agent.agents.research.user_persona_agent import user_persona_agent, user_persona_agent_async
from deep_research_agent.agents.research.search_summarizer_agent import SearchSummarizerAgent
from deep_research_agent.agents.ideation.ideation_agent import IdeationAgent
from deep_research_agent.agents.ideation.devils_advocate_agent import DevilsAdvocateAgent
from deep_research_agent.agents.evaluation.evaluation_coordinator_agent import EvaluationCoordinatorAgent
from deep_research_agent.agents.evaluation.ranking_agent import RankingAgent
from deep_research_agent.agents.reporting.report_synthesizer_agent import ReportSynthesizerAgent


class OrchestratorAgent:
    def __init__(self):
        # Create a BedrockModel with explicit region specification
        model = BedrockModel(
            model_id="us.anthropic.claude-3-7-sonnet-20250219-v1:0",
            region_name="us-east-1"  # Explicitly specify the region
        )
        self._agent = Agent(model=model)

    async def run_research_agents_parallel(self, mission_brief: MissionBrief):
        """
        Run all research agents in parallel for faster execution.
        """
        print("Starting parallel research phase...")
        
        # Create coroutines for all research agents using async versions with shared agent
        research_tasks = [
            generic_search_async(mission_brief.decomposed_tasks.generic_search_query, self._agent),
            business_analysis_async(mission_brief.decomposed_tasks.business_analysis_query, self._agent),
            domain_search_async(mission_brief.decomposed_tasks.domain_specific_query, self._agent),
            trend_spotter_async(mission_brief.decomposed_tasks.trend_spotter_query, self._agent),
            user_persona_agent_async(mission_brief, self._agent)
        ]
        
        # Run all research agents in parallel
        research_results = await asyncio.gather(
            *research_tasks,
            return_exceptions=True
        )
        
        # Handle any exceptions that might have occurred and convert to strings
        processed_results = []
        agent_names = ["Generic Search", "Business Analysis", "Domain Search", "Trend Spotter", "User Persona"]
        
        for i, result in enumerate(research_results):
            if isinstance(result, Exception):
                print(f"Warning: {agent_names[i]} agent failed with error: {result}")
                processed_results.append(f"Error in {agent_names[i]}: {str(result)}")
            else:
                processed_results.append(str(result))
        
        print("Parallel research phase completed!")
        return processed_results

    def run_workflow(self, initial_prompt: str, user_refinement: str):
        # 1. Query Enrichment Layer
        clarifier_agent = ClarifierAgent(agent=self._agent)
        clarifying_questions = clarifier_agent.execute(initial_prompt)
        print(f"Clarifying Questions:\n{clarifying_questions}\n")

        conversation_history = [initial_prompt, clarifying_questions, user_refinement]
        summarizer_agent = ConversationSummarizerAgent(agent=self._agent)
        summary = summarizer_agent.execute(conversation_history)
        print(f"Conversation Summary:\n{summary}\n")

        enhancer_agent = QueryEnhancerAgent(agent=self._agent)
        enhanced_prompt = enhancer_agent.execute(summary)
        print(f"Enhanced Prompt:\n{enhanced_prompt}\n")

        understanding_agent = QueryUnderstandingAgent(agent=self._agent)
        mission_brief = understanding_agent.execute(enhanced_prompt)
        print(f"Mission Brief:\n{mission_brief.model_dump_json(indent=2)}\n")

        # 2. Comprehensive Research Phase - Now Running in Parallel!
        research_results = asyncio.run(self.run_research_agents_parallel(mission_brief))
        generic_report, business_report, domain_report, trend_report, personas = research_results

        search_summarizer_agent = SearchSummarizerAgent(agent=self._agent)
        creative_brief = search_summarizer_agent.execute([
            generic_report, business_report, domain_report, trend_report, personas
        ])
        print(f"Creative Brief:\n{creative_brief}\n")

        # 3. Dynamic Ideation & Refinement Cycle
        ideation_agent = IdeationAgent(agent=self._agent)
        initial_ideas = ideation_agent.execute(creative_brief)
        print(f"Initial Ideas:\n{initial_ideas}\n")

        devils_advocate_agent = DevilsAdvocateAgent(agent=self._agent)
        feedback = devils_advocate_agent.execute(initial_ideas)
        print(f"Devil's Advocate Feedback:\n{feedback}\n")

        refined_ideas = ideation_agent.execute(creative_brief, feedback=feedback)
        print(f"Refined Ideas:\n{refined_ideas}\n")

        # 4. Multi-Faceted Evaluation Phase
        eval_coordinator = EvaluationCoordinatorAgent(agent=self._agent)
        scored_ideas = eval_coordinator.execute(refined_ideas)
        
        ranking_agent = RankingAgent(agent=self._agent)
        ranked_ideas = ranking_agent.execute(scored_ideas)
        print(f"Ranked Ideas:\n{ranked_ideas}\n")

        # 5. Reporting Phase
        report_synthesizer = ReportSynthesizerAgent(agent=self._agent)
        final_report = report_synthesizer.execute(ranked_ideas, creative_brief)
        print(f"Final Report:\n{final_report}")
        
        return final_report

