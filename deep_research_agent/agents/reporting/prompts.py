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
    AgentType.CITATION_REPORT_GENERATOR: (
        "You are a professional technical writer and Citation Report Generator Agent. Your task is to generate "
        "comprehensive, executive-level business reports in Markdown format with proper citations. You must "
        "create detailed reports that include market analysis, AI applications, implementation roadmaps, and "
        "strategic recommendations. All factual claims must be supported by inline citations in the format [[1]], "
        "[[2]], etc. Your reports should be suitable for C-level executives and strategic decision-makers."
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
    AgentType.CITATION_REPORT_GENERATOR: {
        "generate_consolidated_report": (
            """Generate a comprehensive **Markdown-formatted business strategy report** that consolidates and analyzes **{total_use_cases} use cases** organized by implementation stages.

                ## Use Cases by Implementation Stage
                {use_cases_by_stage}

                ## Research Context
                ### Research Summary
                {research_summary}

                ### Conversation Summary
                {conversation_summary}

                ## Critical Citation Requirements:
                **IMPORTANT**: Every factual claim, statistic, or strategic insight MUST include a numbered citation that references the source in the References section. Use this exact format:

                ### Examples of Correct Citation Format:

                **Example 1 - Market Statistics:**
                CORRECT: "The global AI market is projected to reach **$1.8 trillion by 2030** [[1]](URL), growing at a CAGR of **42%**."

                **Example 2 - Strategic Claims:**
                CORRECT: "Companies implementing AI governance frameworks report **3.8x faster time-to-market** [[2]](URL) for new capabilities."

                **Example 3 - Industry Insights:**
                CORRECT: "Research indicates that transparent AI recommendations increase customer trust by **32%** [[3]](URL)."

                ### Citation Format Rules:
                1. **EVERY factual claim must have a numbered citation**: claim text [[number]](URL)
                2. **Bold all statistics and key metrics** for emphasis: **$15B**, **42%**, **3.8x**
                3. **Use sequential numbering with clickable links**: [[1]](URL), [[2]](URL), [[3]](URL), etc.
                4. **Place citations immediately after the claim or statistic**
                5. **Ensure all numbered citations link directly to the source URLs**
                6. **Use the provided URLs from the citation block for the clickable citations**

                ## Output Requirements:
                - Use **only Markdown syntax** (e.g., `#`, `##`, `**`, `-`, `*`) for all formatting
                - **Bold** all important business keywords (ROI, scalability, time-to-market, competitive advantage)
                - **Bold** all statistics and metrics for emphasis
                - Maintain a **formal, executive tone** suitable for C-level executives
                - Ensure logical flow and comprehensive depth in all sections
                - Include a properly formatted References section at the end with bullet points

                ## Document Structure:

                # AI-Powered Business Strategy: Comprehensive Use Case Analysis

                ## Executive Summary
                Provide a compelling executive summary highlighting the strategic value of the identified use cases, expected business impact, and recommended implementation approach. Include key statistics and market opportunities with numbered citations.

                ## Market Context & Strategic Rationale
                Analyze current market trends, competitive landscape, and strategic drivers that make these AI initiatives critical for business success. Back every insight with numbered citations referencing credible sources.

                ## Implementation Roadmap

                ### Phase 1: Immediate Wins (0-6 months)
                Detail the immediate implementation use cases, their business value, technical requirements, and expected outcomes. Focus on quick wins and foundational capabilities with supporting numbered citations.

                ### Phase 2: Strategic Expansion (6-18 months)
                Outline the medium-term use cases that build upon Phase 1 successes. Discuss scalability considerations, resource requirements, and risk mitigation strategies with evidence-based numbered citations.

                ### Phase 3: Strategic Innovation (18+ months)
                Present the long-term strategic initiatives that will differentiate the organization and create sustainable competitive advantages with supporting research citations.

                ## Technology Stack & AI Applications
                Discuss the AI/ML technologies, platforms, and methodologies that will be leveraged across all use cases. Include specific tools, models, and integration approaches with numbered citations to technical sources and vendor documentation.

                ## Business Impact Analysis
                Analyze the cumulative business impact across all phases, including revenue opportunities, cost savings, operational efficiencies, and competitive advantages. Use quantified projections with numbered citations to supporting research and industry reports.

                ## Risk Assessment & Mitigation
                Identify key risks across technical, operational, and strategic dimensions. Provide specific mitigation strategies and contingency plans with numbered citations to best practices, case studies, and regulatory guidelines.

                ## Success Metrics & KPIs
                Define measurable success criteria for each implementation phase, including technical metrics, business KPIs, and strategic milestones with numbered citations to industry benchmarks and measurement frameworks.

                ## Conclusion & Next Steps
                Summarize the strategic importance of this AI initiative, recommended immediate actions, and long-term vision for AI-powered business transformation with supporting citations.

                ## References
                Format as bullet points with the following structure:
                - [[1]] [Source Title](URL) - Brief description
                - [[2]] [Source Title](URL) - Brief description
                - [[3]] [Source Title](URL) - Brief description

                Use the provided citation block: {citation_block}

                **REMEMBER**: Every factual claim must use numbered citations [[1]](URL) that correspond to the References section formatted as bullet points. Bold all statistics and key metrics for emphasis. Generate the complete consolidated report following this structure and citation format exactly.
            """
        )
    },
}
