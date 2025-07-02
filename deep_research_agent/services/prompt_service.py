from typing import Dict, Optional
from deep_research_agent.common.schemas import AgentType

# Explicit imports for all prompts modules
from deep_research_agent.agents.ideation import prompts as ideation_prompts
from deep_research_agent.agents.research import prompts as research_prompts
from deep_research_agent.agents.reporting import prompts as reporting_prompts
from deep_research_agent.agents.evaluation import prompts as evaluation_prompts
from deep_research_agent.agents.query_enrichment import prompts as query_enrichment_prompts


class PromptService:
    """Centralized service for managing all agent prompts"""

    def __init__(self):
        """
        Initialize the prompt service by loading prompts from explicitly imported modules.
        This approach ensures all prompts are loaded correctly and fails fast if any are missing.
        """
        self._system_prompts: Dict[AgentType, str] = {}
        self._user_prompt_templates: Dict[AgentType, Dict[str, str]] = {}
        self._initialize_prompts()

    def _initialize_prompts(self):
        """
        Load prompts from explicitly imported modules with validation.
        This replaces the fragile dynamic discovery approach.
        """
        # List of all prompts modules to load
        prompts_modules = [
            ideation_prompts,
            research_prompts,
            reporting_prompts,
            evaluation_prompts,
            query_enrichment_prompts
        ]
        
        # Load prompts from each module
        for module in prompts_modules:
            self._load_module_prompts(module)
        
        # Validate that we have prompts for all agent types
        self._validate_prompts()

    def _load_module_prompts(self, module):
        """Load prompts from a specific module"""
        if hasattr(module, "SYSTEM_PROMPTS") and isinstance(module.SYSTEM_PROMPTS, dict):
            self._system_prompts.update(module.SYSTEM_PROMPTS)
        
        if hasattr(module, "USER_PROMPT_TEMPLATES") and isinstance(module.USER_PROMPT_TEMPLATES, dict):
            self._user_prompt_templates.update(module.USER_PROMPT_TEMPLATES)

    def _validate_prompts(self):
        """
        Validate that we have system prompts for all agent types.
        This helps catch missing prompts early.
        """
        missing_system_prompts = []
        for agent_type in AgentType:
            if agent_type not in self._system_prompts:
                missing_system_prompts.append(agent_type.value)
        
        if missing_system_prompts:
            raise ValueError(
                f"Missing system prompts for agent types: {', '.join(missing_system_prompts)}. "
                f"Please ensure all agent types have corresponding prompts defined."
            )

    def get_system_prompt(self, agent_type: AgentType) -> str:
        """Get the system prompt for a specific agent type"""
        return self._system_prompts.get(agent_type, "")

    def get_user_prompt_template(self, agent_type: AgentType, template_name: str) -> Optional[str]:
        """Get a user prompt template for a specific agent type and template name"""
        agent_templates = self._user_prompt_templates.get(agent_type, {})
        return agent_templates.get(template_name)

    def format_user_prompt(self, agent_type: AgentType, template_name: str, **kwargs) -> str:
        """Format a user prompt template with provided keyword arguments"""
        template = self.get_user_prompt_template(agent_type, template_name)
        if not template:
            raise ValueError(f"Template '{template_name}' not found for agent type '{agent_type.value}'")
        return template.format(**kwargs)

    def get_available_templates(self, agent_type: AgentType) -> list[str]:
        """Get list of available template names for a specific agent type"""
        return list(self._user_prompt_templates.get(agent_type, {}).keys())

    def add_system_prompt(self, agent_type: AgentType, prompt: str) -> None:
        """Add or update a system prompt for an agent type (primarily for testing)"""
        self._system_prompts[agent_type] = prompt

    def add_user_prompt_template(self, agent_type: AgentType, template_name: str, template: str) -> None:
        """Add or update a user prompt template for an agent type (primarily for testing)"""
        if agent_type not in self._user_prompt_templates:
            self._user_prompt_templates[agent_type] = {}
        self._user_prompt_templates[agent_type][template_name] = template