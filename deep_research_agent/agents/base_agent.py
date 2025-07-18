from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from deep_research_agent.services.prompt_service import PromptService


class BaseAgent(ABC):
    """Abstract base class for all agents in the system."""

    def __init__(self, prompt_service: "PromptService | None" = None):
        """
        Initialize the base agent.

        Args:
            prompt_service: Optional service for retrieving prompts
        """
        self.prompt_service = prompt_service

    @abstractmethod
    def execute(self, context: dict[str, Any]):
        """
        Execute the agent's main functionality.

        Args:
            context: Shared context dictionary containing workflow data
        """
        pass
