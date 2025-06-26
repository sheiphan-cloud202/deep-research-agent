from abc import ABC, abstractmethod
from strands import Agent


class BaseAgent(ABC):
    def __init__(self, agent: Agent):
        self._agent = agent

    @abstractmethod
    def execute(self, *args, **kwargs):
        pass 