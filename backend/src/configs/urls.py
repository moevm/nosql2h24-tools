import os.path

from pydantic_settings import BaseSettings, SettingsConfigDict

config_dir = os.path.dirname(os.path.abspath(__file__))

class Urls(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=os.path.join(config_dir, "../../env/.env.urls"),
        env_file_encoding='utf-8',
        extra="ignore"
    )

    backend_base_url: str
    frontend_base_url: str
    api_prefix: str