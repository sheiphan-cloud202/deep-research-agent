import json
import re
from typing import Any

from deep_research_agent.agents.base_agent import BaseAgent
from deep_research_agent.common.config import settings
from deep_research_agent.common.schemas import AgentType, UseCase, UseCases
from deep_research_agent.core.agent_factory import AgentFactory
from deep_research_agent.services.prompt_service import PromptService
from deep_research_agent.utils.logger import logger


class IdeationAgent(BaseAgent):
    def __init__(self, prompt_service: PromptService, model_id: str | None = None):
        super().__init__(prompt_service)
        self._agent = AgentFactory.create_agent(model_id or settings.claude_3_5_sonnet_model_id)
        if self.prompt_service:
            self._agent.system_prompt = self.prompt_service.get_system_prompt(AgentType.IDEATION)

    def execute(self, context: dict[str, Any]):
        if not self.prompt_service:
            raise ValueError("PromptService is not available for IdeationAgent")

        creative_brief = context["creative_brief"]
        feedback = context.get("devils_advocate_feedback")

        if feedback:
            # This is the second pass, refining ideas
            prompt = self.prompt_service.format_user_prompt(
                AgentType.IDEATION,
                "refine_with_feedback",
                creative_brief=creative_brief,
                feedback=feedback,
            )
            result = self._agent(prompt)
            # Parse JSON and convert to UseCases
            parsed_result = self._parse_json_to_usecases(str(result))
            context["refined_ideas"] = parsed_result
            logger.info(f"Refined Ideas:\n{parsed_result.model_dump_json(indent=2)}\n")
        else:
            # This is the first pass, generating initial ideas
            prompt = self.prompt_service.format_user_prompt(
                AgentType.IDEATION, "generate_initial", creative_brief=creative_brief
            )
            result = self._agent(prompt)
            # Parse JSON and convert to UseCases
            parsed_result = self._parse_json_to_usecases(str(result))
            context["initial_ideas"] = parsed_result
            logger.info(f"Initial Ideas:\n{parsed_result.model_dump_json(indent=2)}\n")

    def _parse_json_to_usecases(self, response_text: str) -> UseCases:
        """Parse the agent's text response and convert it to UseCases object."""
        try:
            # Try to extract JSON from the response
            json_match = re.search(r"\{.*\}", response_text, re.DOTALL)
            if json_match:
                json_text = json_match.group()
                data = json.loads(json_text)
            else:
                # If no JSON found, try to parse the entire response
                data = json.loads(response_text)

            # Handle different possible JSON structures
            if isinstance(data, dict):
                if "use_cases" in data:
                    # Already in the expected format
                    return UseCases.model_validate(data)
                elif isinstance(data, dict) and all(isinstance(v, dict) for v in data.values()):
                    # Convert dict of use cases to list format
                    use_cases_list = []
                    for key, use_case_data in data.items():
                        if not use_case_data.get("id"):
                            use_case_data["id"] = key
                        use_cases_list.append(UseCase.model_validate(use_case_data))
                    return UseCases(use_cases=use_cases_list)
            elif isinstance(data, list):
                # Direct list of use cases
                use_cases_list = [UseCase.model_validate(item) for item in data]
                return UseCases(use_cases=use_cases_list)

        except (json.JSONDecodeError, ValueError, KeyError) as e:
            logger.error(f"Failed to parse JSON response: {e}")
            logger.error(f"Response text: {response_text}")

        # Fallback: create a default structure if parsing fails
        logger.warning("Failed to parse response, creating default structure")
        return UseCases(use_cases=[])
