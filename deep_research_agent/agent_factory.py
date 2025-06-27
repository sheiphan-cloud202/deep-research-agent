from typing import Optional
from strands import Agent
from strands.models import BedrockModel
from botocore.config import Config


class AgentFactory:
    _default_agent: Optional[Agent] = None

    @classmethod
    def get_default_agent(cls) -> Agent:
        if cls._default_agent is None:
            config = Config(
                connect_timeout=900,
                read_timeout=900
            )
            model = BedrockModel(
                model_id="us.anthropic.claude-3-7-sonnet-20250219-v1:0",
                region_name="us-east-1",
                boto_client_config=config
            )
            cls._default_agent = Agent(model=model)
        return cls._default_agent

    @classmethod
    def create_agent(cls, model_id: Optional[str] = None) -> Agent:
        config = Config(
            connect_timeout=900,
            read_timeout=900
        )
        if model_id:
            model = BedrockModel(
                model_id=model_id,
                region_name="us-east-1",
                boto_client_config=config
            )
            return Agent(model=model)
        return cls.get_default_agent()