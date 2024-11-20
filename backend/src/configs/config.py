from pydantic_settings import BaseSettings, SettingsConfigDict

from src.configs.collection_config import CollectionConfig
from src.configs.jwt_config import JWTConfig
from src.configs.mongo_config import MongoConfig
from src.configs.static_paths import StaticPaths


class Config(BaseSettings):
    model_config = SettingsConfigDict(
        env_file="src/.env",
        env_file_encoding='utf-8',
        extra="ignore"
    )

    mongo: MongoConfig = MongoConfig()
    jwt: JWTConfig = JWTConfig()
    collections: CollectionConfig = CollectionConfig()
    static_paths: StaticPaths = StaticPaths()

config = Config()

