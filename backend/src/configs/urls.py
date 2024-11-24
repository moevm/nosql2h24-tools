from pydantic_settings import BaseSettings, SettingsConfigDict

class Urls(BaseSettings):
    model_config = SettingsConfigDict(
        env_file="env/.env.urls",
        env_file_encoding='utf-8',
        extra="ignore"
    )

    backend_base_url: str
    frontend_base_url: str
    api_prefix: str