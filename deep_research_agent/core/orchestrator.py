import inspect
from datetime import datetime
from typing import Any

from deep_research_agent.common.schemas import AgentType
from deep_research_agent.core.agent_registry import AGENT_REGISTRY
from deep_research_agent.core.workflow import DEFAULT_WORKFLOW, WORKFLOW_STEP_METADATA, get_workflow_metadata
from deep_research_agent.services.prompt_service import PromptService
from deep_research_agent.utils.logger import logger


class OrchestratorAgent:
    def __init__(self, workflow: list | None = None):
        self.prompt_service = PromptService()
        self.workflow_context = {}  # Stores the outputs of each step
        self.workflow = workflow if workflow else DEFAULT_WORKFLOW
        self.current_step = 0

        # Enhanced progress tracking
        self.workflow_status = {
            "status": "initialized",  # initialized, running, completed, error, awaiting_input
            "current_step": 0,
            "total_steps": len(self.workflow),
            "current_agent": None,
            "started_at": None,
            "completed_at": None,
            "step_history": [],
            "progress_percentage": 0.0,
            "last_updated": datetime.utcnow().isoformat(),
            "workflow_metadata": get_workflow_metadata(self.workflow),
        }

    def get_workflow_status(self) -> dict[str, Any]:
        """Get the current workflow status and progress"""
        current_step_metadata = None
        if self.current_step < len(self.workflow):
            agent_type = self.workflow[self.current_step]
            current_step_metadata = WORKFLOW_STEP_METADATA.get(agent_type, {})

        return {
            **self.workflow_status,
            "workflow_context_keys": list(self.workflow_context.keys()),
            "context_summary": self._get_context_summary(),
            "current_step_metadata": current_step_metadata,
        }

    def _get_context_summary(self) -> dict[str, Any]:
        """Get a summary of the current workflow context"""
        summary = {}
        for key, value in self.workflow_context.items():
            if isinstance(value, list):
                summary[key] = f"List with {len(value)} items"
            elif isinstance(value, dict):
                summary[key] = f"Dict with keys: {list(value.keys())}"
            elif isinstance(value, str):
                summary[key] = f"String (length: {len(value)})"
            else:
                summary[key] = str(type(value).__name__)
        return summary

    def _update_status(self, status: str, agent_type: AgentType | None = None):
        """Update the workflow status"""
        self.workflow_status.update(
            {
                "status": status,
                "current_step": self.current_step,
                "current_agent": agent_type.value if agent_type else None,
                "progress_percentage": (self.current_step / self.workflow_status["total_steps"]) * 100,
                "last_updated": datetime.utcnow().isoformat(),
            }
        )

    async def start_workflow(self, initial_prompt: str):
        # Preserve existing context (like uploaded_files) and add conversation history
        if not hasattr(self, "workflow_context") or self.workflow_context is None:
            self.workflow_context = {}

        self.workflow_context["conversation_history"] = [initial_prompt]
        self.current_step = 0

        # Initialize workflow tracking
        self.workflow_status.update(
            {"status": "running", "started_at": datetime.utcnow().isoformat(), "step_history": []}
        )
        self._update_status("running")

        return await self.run_next_step()

    async def continue_workflow(self, user_response: str):
        self.workflow_context["conversation_history"].append(user_response)
        self._update_status("running")
        return await self.run_next_step()

    async def run_next_step(self):
        if self.current_step >= len(self.workflow):
            # Get use cases from ideation agent (initial_ideas or refined_ideas)
            use_cases = self.workflow_context.get("refined_ideas") or self.workflow_context.get("initial_ideas")
            serialized_use_cases = self._serialize_use_cases(use_cases)

            # Mark workflow as completed
            self.workflow_status.update(
                {"status": "completed", "completed_at": datetime.utcnow().isoformat(), "progress_percentage": 100.0}
            )
            self._update_status("completed")

            logger.info("\n--- END OF WORKFLOW ---")
            logger.info(f"Use Cases from Ideation Agent:\n{use_cases}")
            return {"use_cases": serialized_use_cases}

        agent_type = self.workflow[self.current_step]
        try:
            await self._execute_step(agent_type)
        except Exception as e:
            # Record the error in workflow status
            self.workflow_status.update(
                {"status": "error", "error": str(e), "error_step": self.current_step, "error_agent": agent_type.value}
            )
            self._update_status("error", agent_type)
            raise

        self.current_step += 1
        return await self.run_next_step()

    async def run_workflow_from_conversation(self, conversation_history: list):
        """
        Run the complete, dynamically configured workflow using conversation history.
        """
        self.workflow_context = {"conversation_history": conversation_history}

        # Initialize workflow tracking
        self.workflow_status.update(
            {"status": "running", "started_at": datetime.utcnow().isoformat(), "step_history": []}
        )
        self._update_status("running")

        for step_index, step in enumerate(self.workflow):
            self.current_step = step_index
            await self._execute_step(step)

        # Mark workflow as completed
        self.workflow_status.update(
            {"status": "completed", "completed_at": datetime.utcnow().isoformat(), "progress_percentage": 100.0}
        )
        self._update_status("completed")

        # Get use cases from ideation agent (initial_ideas or refined_ideas)
        use_cases = self.workflow_context.get("refined_ideas") or self.workflow_context.get("initial_ideas")
        serialized_use_cases = self._serialize_use_cases(use_cases)
        logger.info("\n--- END OF WORKFLOW ---")
        logger.info(f"Use Cases from Ideation Agent:\n{use_cases}")
        return serialized_use_cases

    async def _execute_step(self, agent_type: AgentType):
        step_start_time = datetime.utcnow()

        logger.info(f"--- Executing Step: {agent_type.value} ---")
        self._update_status("running", agent_type)

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

        try:
            if inspect.iscoroutinefunction(agent_instance.execute):
                await agent_instance.execute(self.workflow_context)
            else:
                agent_instance.execute(self.workflow_context)

            # Record successful step completion
            step_end_time = datetime.utcnow()
            step_duration = (step_end_time - step_start_time).total_seconds()

            step_record = {
                "step": self.current_step,
                "agent_type": agent_type.value,
                "status": "completed",
                "started_at": step_start_time.isoformat(),
                "completed_at": step_end_time.isoformat(),
                "duration_seconds": step_duration,
            }

            self.workflow_status["step_history"].append(step_record)

        except Exception as e:
            # Record failed step
            step_end_time = datetime.utcnow()
            step_duration = (step_end_time - step_start_time).total_seconds()

            step_record = {
                "step": self.current_step,
                "agent_type": agent_type.value,
                "status": "error",
                "started_at": step_start_time.isoformat(),
                "error_at": step_end_time.isoformat(),
                "duration_seconds": step_duration,
                "error": str(e),
            }

            self.workflow_status["step_history"].append(step_record)
            raise

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
