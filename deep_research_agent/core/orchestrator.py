import inspect

from deep_research_agent.common.schemas import AgentType
from deep_research_agent.core.agent_registry import AGENT_REGISTRY
from deep_research_agent.core.workflow import DEFAULT_WORKFLOW
from deep_research_agent.services.prompt_service import PromptService
from deep_research_agent.utils.logger import logger


class OrchestratorAgent:
    def __init__(self, workflow: list | None = None):
        self.prompt_service = PromptService()
        self.workflow_context = {}  # Stores the outputs of each step
        self.workflow = workflow if workflow else DEFAULT_WORKFLOW
        self.current_step = 0

    async def start_workflow(self, initial_prompt: str):
        # Preserve existing context (like uploaded_files) and add conversation history
        if not hasattr(self, "workflow_context") or self.workflow_context is None:
            self.workflow_context = {}
        self.workflow_context["conversation_history"] = [initial_prompt]
        self.current_step = 0
        return await self.run_next_step()

    async def continue_workflow(self, user_response: str):
        self.workflow_context["conversation_history"].append(user_response)
        return await self.run_next_step()

    async def run_next_step(self):
        if self.current_step >= len(self.workflow):
            # Get use cases from ideation agent (initial_ideas or refined_ideas)
            use_cases = self.workflow_context.get("refined_ideas") or self.workflow_context.get("initial_ideas")
            serialized_use_cases = self._serialize_use_cases(use_cases)
            logger.info("\n--- END OF WORKFLOW ---")
            logger.info(f"Use Cases from Ideation Agent:\n{use_cases}")
            return {"use_cases": serialized_use_cases}

        agent_type = self.workflow[self.current_step]
        await self._execute_step(agent_type)

        self.current_step += 1
        return await self.run_next_step()

    async def run_workflow_from_conversation(self, conversation_history: list):
        """
        Run the complete, dynamically configured workflow using conversation history.
        """
        self.workflow_context = {"conversation_history": conversation_history}

        for step in self.workflow:
            await self._execute_step(step)

        # Get use cases from ideation agent (initial_ideas or refined_ideas)
        use_cases = self.workflow_context.get("refined_ideas") or self.workflow_context.get("initial_ideas")
        serialized_use_cases = self._serialize_use_cases(use_cases)
        logger.info("\n--- END OF WORKFLOW ---")
        logger.info(f"Use Cases from Ideation Agent:\n{use_cases}")
        return serialized_use_cases

    async def _execute_step(self, agent_type: AgentType):
        logger.info(f"--- Executing Step: {agent_type.value} ---")
        agent_class = AGENT_REGISTRY.get(agent_type)
        if not agent_class:
            raise ValueError(f"No agent found for agent type: {agent_type.value}")

        # Instantiate the agent, passing prompt_service if it's a required parameter
        try:
            # Check if the agent's __init__ accepts 'prompt_service'
            sig = inspect.signature(agent_class.__init__)
            if "prompt_service" in sig.parameters:
                agent_instance = agent_class(prompt_service=self.prompt_service)
            else:
                agent_instance = agent_class()
        except Exception as e:
            logger.error(f"Failed to instantiate agent {agent_class.__name__}: {e}")
            raise

        if inspect.iscoroutinefunction(agent_instance.execute):
            await agent_instance.execute(self.workflow_context)
        else:
            agent_instance.execute(self.workflow_context)

    def _serialize_use_cases(self, use_cases):
        """
        Serialize use cases from ideation agent for JSON response.
        Converts UseCases object to JSON-serializable format.
        """
        if not use_cases:
            return []

        if hasattr(use_cases, "model_dump"):
            # UseCases object with model_dump method
            return use_cases.model_dump()["use_cases"]
        elif hasattr(use_cases, "use_cases"):
            # UseCases object without model_dump
            return [uc.model_dump() if hasattr(uc, "model_dump") else uc for uc in use_cases.use_cases]
        else:
            # Fallback for other formats
            return use_cases
