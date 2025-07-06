from abc import ABC, abstractmethod
from typing import Any

from deep_research_agent.services.prompt_service import PromptService


class BaseAgent(ABC):
    """Abstract base class for all agents in the system."""

    def __init__(self, prompt_service: PromptService | None = None):
        self.prompt_service = prompt_service

    @abstractmethod
    def execute(self, context: dict[str, Any]) -> None:
        """
        Execute the agent's primary logic.

        This method should read data from the context, perform its operations,
        and write its output back to the context.
        """
        pass
