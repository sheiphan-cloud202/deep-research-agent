from typing import Optional
from strands import Agent
from strands.models import BedrockModel
from botocore.config import Config
from deep_research_agent.common.config import settings


class AgentFactory:
    _default_agent: Optional[Agent] = None

    @classmethod
    def get_default_agent(cls) -> Agent:
        if cls._default_agent is None:
            config = Config(
                connect_timeout=settings.boto_connect_timeout,
                read_timeout=settings.boto_read_timeout
            )
            model = BedrockModel(
                model_id=settings.default_model_id,
                region_name=settings.aws_region,
                boto_client_config=config
            )
            cls._default_agent = Agent(model=model)
        return cls._default_agent

    @classmethod
    def create_agent(cls, model_id: Optional[str] = None) -> Agent:
        config = Config(
            connect_timeout=settings.boto_connect_timeout,
            read_timeout=settings.boto_read_timeout
        )
        if model_id:
            model = BedrockModel(
                model_id=model_id,
                region_name=settings.aws_region,
                boto_client_config=config
            )
            return Agent(model=model)
        return cls.get_default_agent()