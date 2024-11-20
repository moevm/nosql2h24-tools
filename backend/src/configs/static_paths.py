from pydantic_settings import BaseSettings, SettingsConfigDict

class StaticPaths(BaseSettings):
    model_config = SettingsConfigDict(
        env_file="src/.env",
        env_file_encoding='utf-8',
        extra="ignore"
    )

    api_uri_prefix: str
    tool_img_storage_prefix_path: str
    client_img_storage_prefix_path: str
    worker_img_storage_prefix_path: str
