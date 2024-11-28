import os
from pydantic_settings import BaseSettings, SettingsConfigDict

config_dir = os.path.dirname(os.path.abspath(__file__))

class Paths(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=os.path.join(config_dir, "../../env/.env.paths"),
        env_file_encoding='utf-8',
        extra="ignore"
    )

    tool_img_storage_prefix_path: str
    client_img_storage_prefix_path: str
    worker_img_storage_prefix_path: str
    image_dir: str
