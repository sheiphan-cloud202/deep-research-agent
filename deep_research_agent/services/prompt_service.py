from typing import Dict, Optional
import importlib.util
import pkgutil
from pathlib import Path
from deep_research_agent.common.schemas import AgentType


class PromptService:
    """Centralized service for managing all agent prompts"""

    def __init__(self, agents_package_path: str = "deep_research_agent/agents"):
        """
        Initialize the prompt service by dynamically loading prompts.
        
        :param agents_package_path: The file path to the 'agents' package.
        """
        self._system_prompts: Dict[AgentType, str] = {}
        self._user_prompt_templates: Dict[AgentType, Dict[str, str]] = {}
        self._initialize_prompts(agents_package_path)

    def _initialize_prompts(self, agents_package_path: str):
        """
        Dynamically discover and load prompts from all 'prompts.py' files
        within the specified agents package path.
        """
        package_path = Path(agents_package_path)
        package_name = ".".join(package_path.parts)

        for module_info in pkgutil.walk_packages([str(package_path)], prefix=f"{package_name}."):
            if module_info.name.endswith(".prompts"):
                module = importlib.import_module(module_info.name)
                
                if hasattr(module, "SYSTEM_PROMPTS") and isinstance(module.SYSTEM_PROMPTS, dict):
                    self._system_prompts.update(module.SYSTEM_PROMPTS)
                
                if hasattr(module, "USER_PROMPT_TEMPLATES") and isinstance(module.USER_PROMPT_TEMPLATES, dict):
                    self._user_prompt_templates.update(module.USER_PROMPT_TEMPLATES)

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