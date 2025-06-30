from abc import ABC, abstractmethod
from typing import Optional
from strands import Agent
from deep_research_agent.agent_factory import AgentFactory


class BaseAgent(ABC):
    def __init__(self, agent: Optional[Agent] = None, model_id: Optional[str] = None):
        if agent:
            self._agent = agent
        else:
            self._agent = AgentFactory.create_agent(model_id)

    @abstractmethod
    def execute(self, *args, **kwargs):
        pass
    
    def set_system_prompt_from_service(self, agent_type):
        """Helper method to set system prompt from the prompt service"""
        from deep_research_agent.prompt_service import PromptService
        self._agent.system_prompt = PromptService.get_system_prompt(agent_type)
    
    def format_user_prompt(self, agent_type, template_name: str, **kwargs) -> str:
        """Helper method to format user prompts using the prompt service"""
        from deep_research_agent.prompt_service import PromptService
        return PromptService.format_user_prompt(agent_type, template_name, **kwargs) 