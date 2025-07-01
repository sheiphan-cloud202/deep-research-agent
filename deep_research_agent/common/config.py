from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', extra='ignore')

    # AWS Configuration
    aws_region: str = "us-east-1"

    # Bedrock Model IDs
    default_model_id: str = "us.anthropic.claude-3-7-sonnet-20250219-v1:0"
    claude_sonnet_model_id: str = "anthropic.claude-3-5-sonnet-20240620-v1:0"

    # Boto3 Client Configuration
    boto_connect_timeout: int = 900
    boto_read_timeout: int = 900

settings = Settings() 