from typing import Dict, Optional
from enum import Enum

# Import prompts from respective folders
from deep_research_agent.agents.evaluation import prompts as evaluation_prompts
from deep_research_agent.agents.ideation import prompts as ideation_prompts
from deep_research_agent.agents.query_enrichment import prompts as query_enrichment_prompts
from deep_research_agent.agents.reporting import prompts as reporting_prompts
from deep_research_agent.agents.research import prompts as research_prompts


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


class PromptService:
    """Centralized service for managing all agent prompts"""
    
    # Initialize system prompts by combining all prompt modules
    _system_prompts: Dict[AgentType, str] = {}
    _user_prompt_templates: Dict[AgentType, Dict[str, str]] = {}
    
    @classmethod
    def _initialize_prompts(cls):
        """Initialize prompts from distributed prompt files"""
        if cls._system_prompts:  # Already initialized
            return
            
        # Combine system prompts from all modules
        all_system_prompts = {}
        all_system_prompts.update(evaluation_prompts.SYSTEM_PROMPTS)
        all_system_prompts.update(ideation_prompts.SYSTEM_PROMPTS)
        all_system_prompts.update(query_enrichment_prompts.SYSTEM_PROMPTS)
        all_system_prompts.update(reporting_prompts.SYSTEM_PROMPTS)
        all_system_prompts.update(research_prompts.SYSTEM_PROMPTS)
        
        # Map string keys to AgentType enum
        for agent_type in AgentType:
            if agent_type.value in all_system_prompts:
                cls._system_prompts[agent_type] = all_system_prompts[agent_type.value]
        
        # Combine user prompt templates from all modules
        all_user_templates = {}
        all_user_templates.update(evaluation_prompts.USER_PROMPT_TEMPLATES)
        all_user_templates.update(ideation_prompts.USER_PROMPT_TEMPLATES)
        all_user_templates.update(query_enrichment_prompts.USER_PROMPT_TEMPLATES)
        all_user_templates.update(reporting_prompts.USER_PROMPT_TEMPLATES)
        all_user_templates.update(research_prompts.USER_PROMPT_TEMPLATES)
        
        # Map string keys to AgentType enum
        for agent_type in AgentType:
            if agent_type.value in all_user_templates:
                cls._user_prompt_templates[agent_type] = all_user_templates[agent_type.value]
    
    @classmethod
    def get_system_prompt(cls, agent_type: AgentType) -> str:
        """Get the system prompt for a specific agent type"""
        cls._initialize_prompts()
        return cls._system_prompts.get(agent_type, "")
    
    @classmethod
    def get_user_prompt_template(cls, agent_type: AgentType, template_name: str) -> Optional[str]:
        """Get a user prompt template for a specific agent type and template name"""
        cls._initialize_prompts()
        agent_templates = cls._user_prompt_templates.get(agent_type, {})
        return agent_templates.get(template_name)
    
    @classmethod
    def format_user_prompt(cls, agent_type: AgentType, template_name: str, **kwargs) -> str:
        """Format a user prompt template with provided keyword arguments"""
        cls._initialize_prompts()
        template = cls.get_user_prompt_template(agent_type, template_name)
        if not template:
            raise ValueError(f"Template '{template_name}' not found for agent type '{agent_type.value}'")
        return template.format(**kwargs)
    
    @classmethod
    def get_available_templates(cls, agent_type: AgentType) -> list[str]:
        """Get list of available template names for a specific agent type"""
        cls._initialize_prompts()
        return list(cls._user_prompt_templates.get(agent_type, {}).keys())
    
    @classmethod
    def add_system_prompt(cls, agent_type: AgentType, prompt: str) -> None:
        """Add or update a system prompt for an agent type"""
        cls._initialize_prompts()
        cls._system_prompts[agent_type] = prompt
    
    @classmethod
    def add_user_prompt_template(cls, agent_type: AgentType, template_name: str, template: str) -> None:
        """Add or update a user prompt template for an agent type"""
        cls._initialize_prompts()
        if agent_type not in cls._user_prompt_templates:
            cls._user_prompt_templates[agent_type] = {}
        cls._user_prompt_templates[agent_type][template_name] = template