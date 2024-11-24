from pydantic_settings import BaseSettings, SettingsConfigDict


class CollectionConfig(BaseSettings):
    model_config = SettingsConfigDict(
        env_file="env/.env.collections",
        env_file_encoding='utf-8',
        extra="ignore"
    )

    client_collection: str
    worker_collection: str
    tool_collection: str
    category_collection: str
    type_collection: str
