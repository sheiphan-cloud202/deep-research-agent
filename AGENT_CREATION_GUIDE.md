# How to Create a New Agent

This guide provides a step-by-step process for creating, registering, and integrating a new agent into the deep-research-agent framework.

## Architecture Overview

The system is built around a series of specialized agents that execute in a predefined sequence (workflow). Each agent performs a specific task, reading data from a shared `workflow_context` dictionary and writing its output back into the same dictionary. This modular, context-passing architecture makes it easy to add new capabilities.

## Step-by-Step Guide

Follow these steps to create and integrate a new agent.

### 1. Define the Agent's Role and `AgentType`

First, decide on the agent's purpose and give it a unique identifier.

-   **Action**: Open `deep_research_agent/common/schemas.py`.
-   **Add a new value** to the `AgentType(str, Enum)` class. Group it under an appropriate category (e.g., `# Research`, `# Evaluation`).

**Example**: Let's create a new `ValidationAgent`.

```python
// file: deep_research_agent/common/schemas.py

class AgentType(str, Enum):
    # ... other agent types

    # Evaluation
    # ...
    EVALUATION_COORDINATOR = "evaluation_coordinator"
    VALIDATION_AGENT = "validation_agent" # <-- Add new agent type here

    # Reporting
    # ...
```

### 2. Create the Agent Class

Create a new Python file for your agent in the most relevant sub-directory under `deep_research_agent/agents/`.

-   **Action**: Create a new file (e.g., `deep_research_agent/agents/evaluation/validation_agent.py`).
-   **Content**: Your agent class must inherit from `BaseAgent` and implement the `execute` method.

**Template**:

```python
# file: deep_research_agent/agents/evaluation/validation_agent.py

from typing import Any
from deep_research_agent.agents.base_agent import BaseAgent
from deep_research_agent.common.schemas import AgentType
from deep_research_agent.core.agent_factory import AgentFactory
from deep_research_agent.services.prompt_service import PromptService
from deep_research_agent.utils.logger import logger

class ValidationAgent(BaseAgent):
    def __init__(self, prompt_service: PromptService, model_id: str | None = None):
        super().__init__(prompt_service)
        # Initialize the underlying AI model via the factory
        self._agent = AgentFactory.create_agent(model_id)
        if self.prompt_service:
            # Set the system prompt for this agent
            self._agent.system_prompt = self.prompt_service.get_system_prompt(AgentType.VALIDATION_AGENT)

    def execute(self, context: dict[str, Any]):
        """
        Reads data from the context, performs validation, and writes results back.
        """
        if not self.prompt_service:
            raise ValueError("PromptService is not available for ValidationAgent")

        logger.info("--- Executing Step: Validation ---")

        # 1. Read necessary data from the context
        ideas_to_validate = context.get("ranked_ideas")
        if not ideas_to_validate:
            logger.warning("No ranked ideas found to validate. Skipping.")
            return

        # 2. Prepare the prompt for the AI model
        prompt = self.prompt_service.format_user_prompt(
            AgentType.VALIDATION_AGENT,
            "validate_ideas", # This is a custom template name
            ideas=ideas_to_validate
        )

        # 3. Call the AI model
        validation_results = self._agent(prompt)

        # 4. Write the output back to the context for the next agent
        context["validation_results"] = str(validation_results)
        logger.info("Validation complete. Results added to context.")

```

### 3. Add Prompts for the Agent

Your agent needs instructions (a system prompt) and a template for its queries (a user prompt).

-   **Action**: Open the `prompts.py` file in the same directory as your new agent (e.g., `deep_research_agent/agents/evaluation/prompts.py`).
-   **Add entries** for your new `AgentType` to the `SYSTEM_PROMPTS` and `USER_PROMPT_TEMPLATES` dictionaries.

**Example**:

```python
# file: deep_research_agent/agents/evaluation/prompts.py

# Add to SYSTEM_PROMPTS dictionary
SYSTEM_PROMPTS = {
    # ... other system prompts
    AgentType.VALIDATION_AGENT: (
        "You are a Validation Agent. Your job is to critically assess a list of "
        "ideas and identify potential flaws, risks, or inconsistencies."
    ),
}

# Add to USER_PROMPT_TEMPLATES dictionary
USER_PROMPT_TEMPLATES = {
    # ... other user prompt templates
    AgentType.VALIDATION_AGENT: {
        "validate_ideas": (
            "Please validate the following ideas and provide your critique:\n\n"
            "{ideas}"
        )
    },
}
```

### 4. Register the Agent

The system needs to know that your new agent class exists and which `AgentType` it corresponds to.

-   **Action**: Open `deep_research_agent/core/agent_registry.py`.
-   **Import** your new agent class.
-   **Add an entry** to the `AGENT_REGISTRY` dictionary.

**Example**:

```python
# file: deep_research_agent/core/agent_registry.py

# 1. Import the new agent class
from deep_research_agent.agents.evaluation.validation_agent import ValidationAgent
# ... other imports

AGENT_REGISTRY = {
    # ... other agent registrations
    AgentType.EVALUATION_COORDINATOR: EvaluationCoordinatorAgent,
    AgentType.RANKING: RankingAgent,
    AgentType.VALIDATION_AGENT: ValidationAgent, # <-- 2. Add the registration
    AgentType.REPORT_SYNTHESIZER: ReportSynthesizerAgent,
}
```

### 5. Add the Agent to the Workflow

Finally, insert your agent into the execution pipeline.

-   **Action**: Open `deep_research_agent/core/workflow.py`.
-   **Add your `AgentType`** to the `DEFAULT_WORKFLOW` list in the desired position.

**Example**: Let's add our `ValidationAgent` after the `RankingAgent`.

```python
# file: deep_research_agent/core/workflow.py

DEFAULT_WORKFLOW = [
    # ...
    AgentType.EVALUATION_COORDINATOR,
    AgentType.RANKING,
    AgentType.VALIDATION_AGENT, # <-- Add agent to the workflow
    AgentType.REPORT_SYNTHESIZER,
]
```

### 6. (Optional) Add Dependencies

If your agent requires new third-party libraries (e.g., for parsing a specific file type), add them to the project.

-   **Action**: Open `pyproject.toml`.
-   **Add the package** to the `dependencies` list.
-   **Run `uv sync`** in your terminal to install the new package.

**Example**:

```toml
# file: pyproject.toml
[project]
dependencies = [
    # ... other dependencies
    "new-validation-library>=1.0.0"
]
```

```bash
# In your terminal
uv sync
```

---

You have now successfully created and integrated a new agent. When you run the application, it will be executed as part of the workflow.
