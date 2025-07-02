from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', extra='ignore')

    # AWS Configuration
    aws_region: str = Field(default="us-east-1", alias="AWS_REGION")

    # Bedrock Model IDs
    default_model_id: str = Field(default="us.anthropic.claude-3-7-sonnet-20250219-v1:0", alias="DEFAULT_MODEL_ID")
    claude_sonnet_model_id: str = Field(default="anthropic.claude-3-5-sonnet-20240620-v1:0", alias="CLAUDE_SONNET_MODEL_ID")

    # Boto3 Client Configuration
    boto_connect_timeout: int = Field(default=900, alias="BOTO_CONNECT_TIMEOUT")
    boto_read_timeout: int = Field(default=900, alias="BOTO_READ_TIMEOUT")

settings = Settings() 