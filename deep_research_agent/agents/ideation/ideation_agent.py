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
            # Clean the response text and remove any markdown formatting
            cleaned_text = response_text.strip()
            if cleaned_text.startswith("```json"):
                cleaned_text = cleaned_text[7:]
            if cleaned_text.endswith("```"):
                cleaned_text = cleaned_text[:-3]
            cleaned_text = cleaned_text.strip()

            # Try to extract JSON from the response
            json_match = re.search(r"\{.*\}", cleaned_text, re.DOTALL)
            if json_match:
                json_text = json_match.group()

                # Try to fix incomplete JSON by adding missing closing braces/brackets
                open_braces = json_text.count("{")
                close_braces = json_text.count("}")
                open_brackets = json_text.count("[")
                close_brackets = json_text.count("]")

                # If JSON is incomplete, try to complete it
                if open_braces > close_braces or open_brackets > close_brackets:
                    logger.warning("Detected incomplete JSON, attempting to fix...")

                    # Find the last complete use case
                    use_case_pattern = r'"id":\s*"[^"]*"'
                    matches = list(re.finditer(use_case_pattern, json_text))

                    if matches and len(matches) > 1:
                        # Find the position after the last complete use case
                        last_complete_match = matches[-2]  # Take second-to-last to be safe

                        # Find the end of that use case object
                        search_from = last_complete_match.end()
                        brace_count = 0
                        end_pos = search_from

                        for i, char in enumerate(json_text[search_from:]):
                            if char == "{":
                                brace_count += 1
                            elif char == "}":
                                brace_count -= 1
                                if brace_count == 0:
                                    end_pos = search_from + i + 1
                                    break

                        # Truncate to the last complete use case and close the JSON
                        json_text = json_text[:end_pos] + "]}"
                        logger.info("Truncated JSON to last complete use case")

                data = json.loads(json_text)
            else:
                # If no JSON found, try to parse the entire response
                data = json.loads(cleaned_text)

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
            logger.error(f"Response text (first 1000 chars): {response_text[:1000]}")

            # Try one more time with a more aggressive approach - extract individual use cases
            try:
                use_cases_list = []
                # Look for individual use case objects
                use_case_objects = re.findall(r'\{[^{}]*"id":[^{}]*\}', response_text, re.DOTALL)

                for uc_text in use_case_objects:
                    try:
                        uc_data = json.loads(uc_text)
                        use_cases_list.append(UseCase.model_validate(uc_data))
                    except:  # noqa: E722
                        continue

                if use_cases_list:
                    logger.info(f"Recovered {len(use_cases_list)} use cases from malformed JSON")
                    return UseCases(use_cases=use_cases_list)

            except Exception as fallback_error:
                logger.error(f"Fallback parsing also failed: {fallback_error}")

        # Fallback: create a default structure if parsing fails
        logger.warning("Failed to parse response, creating default structure")
        return UseCases(use_cases=[])
