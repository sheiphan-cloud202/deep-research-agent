# Deep Research Agent

A multi-agent system for deep research using LLM and the strands-agents framework.

## Architecture

The system consists of specialized agents organized into different categories:

- **Evaluation agents**: Assess ideas from different perspectives (ethical, technical, market viability)
- **Ideation agents**: Generate and refine creative ideas
- **Query enrichment agents**: Process and enhance user queries
- **Reporting agents**: Synthesize and present results
- **Research agents**: Gather and analyze information

## Prompt Service

The system includes a modular `PromptService` that manages all system prompts and user prompt templates for consistency and maintainability. Prompts are organized by agent category in their respective folders.

### Features

- **Modular Organization**: Prompts are organized by agent category in separate files
- **Centralized Access**: Single interface to access all prompts regardless of location
- **Template System**: Reusable user prompt templates with parameter substitution
- **Type Safety**: Uses enum-based agent types to prevent errors
- **Extensibility**: Easy to add new prompts and templates

### Usage

```python
from deep_research_agent.prompt_service import PromptService, AgentType

# Get system prompt for an agent
system_prompt = PromptService.get_system_prompt(AgentType.ETHICAL_GUARDIAN)

# Format user prompt with parameters
user_prompt = PromptService.format_user_prompt(
    AgentType.ETHICAL_GUARDIAN,
    "evaluate",
    idea="AI-powered transportation system"
)

# In agent classes
class MyAgent(BaseAgent):
    def __init__(self, agent=None, model_id=None):
        super().__init__(agent, model_id)
        self._agent.system_prompt = PromptService.get_system_prompt(AgentType.MY_AGENT)
    
    def execute(self, data):
        prompt = PromptService.format_user_prompt(
            AgentType.MY_AGENT, 
            "analyze", 
            data=data
        )
        return self._agent.structured_output(MySchema, prompt)
```

### Prompt Organization

Prompts are organized by agent category:

```
deep_research_agent/agents/
├── evaluation/prompts.py        # Ethical, technical, market viability agents
├── ideation/prompts.py          # Ideation and devil's advocate agents  
├── query_enrichment/prompts.py  # Query processing and enhancement agents
├── reporting/prompts.py         # Report synthesis agents
└── research/prompts.py          # Search and analysis agents
```

#### Adding New Prompts

To add prompts for a new agent:

1. **Add to appropriate category file** (e.g., `evaluation/prompts.py`):
```python
SYSTEM_PROMPTS = {
    "my_new_agent": "You are a My New Agent. Your task is to..."
}

USER_PROMPT_TEMPLATES = {
    "my_new_agent": {
        "process": "Process the following data: {data}"
    }
}
```

2. **Add enum value** in `prompt_service.py`:
```python
class AgentType(Enum):
    MY_NEW_AGENT = "my_new_agent"
```

3. **Use in agent class**:
```python
class MyNewAgent(BaseAgent):
    def __init__(self, agent=None, model_id=None):
        super().__init__(agent, model_id)
        self._agent.system_prompt = PromptService.get_system_prompt(AgentType.MY_NEW_AGENT)
```

### Benefits

1. **Consistency**: All agents use standardized prompts
2. **Maintainability**: Prompts organized by domain, easy to find and update
3. **Modularity**: Each agent category manages its own prompts
4. **Reusability**: Templates can be shared across agents
5. **Version Control**: Prompt changes are tracked in code
6. **Testing**: Easier to test different prompt variations

## Development

The system is built using the strands-agents framework and supports various LLM providers through the framework's model abstraction.
