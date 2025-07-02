from abc import ABC, abstractmethod

from strands import Agent

from deep_research_agent.core.agent_factory import AgentFactory


class BaseAgent(ABC):
    def __init__(self, agent: Agent | None = None, model_id: str | None = None):
        if agent:
            self._agent = agent
        else:
            self._agent = AgentFactory.create_agent(model_id)

    @abstractmethod
    def execute(self, *args, **kwargs):
        pass
