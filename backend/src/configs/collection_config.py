import os

from pydantic_settings import BaseSettings, SettingsConfigDict


class CollectionConfig(BaseSettings):
    model_config = SettingsConfigDict(
        env_file="src/.env",
        env_file_encoding='utf-8',
        extra="ignore"
    )

    client_collection: str
    worker_collection: str
