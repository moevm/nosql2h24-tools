from pydantic_settings import BaseSettings, SettingsConfigDict

class Paths(BaseSettings):
    model_config = SettingsConfigDict(
        env_file="env/.env.paths",
        env_file_encoding='utf-8',
        extra="ignore"
    )

    tool_img_storage_prefix_path: str
    client_img_storage_prefix_path: str
    worker_img_storage_prefix_path: str
