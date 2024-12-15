import os.path
from pydantic_settings import BaseSettings, SettingsConfigDict

config_dir = os.path.dirname(os.path.abspath(__file__))


class CollectionConfig(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=os.path.join(config_dir, "../../env/.env.collections"),
        env_file_encoding='utf-8',
        extra="ignore"
    )

    client_collection: str
    worker_collection: str
    tool_collection: str
    category_collection: str
    type_collection: str
    order_collection: str
    review_collection: str