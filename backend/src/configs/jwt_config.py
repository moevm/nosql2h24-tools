import os

from pydantic_settings import BaseSettings, SettingsConfigDict

config_dir = os.path.dirname(os.path.abspath(__file__))

class JWTConfig(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=os.path.join(config_dir, "../../env/.env.jwt"),
        env_file_encoding='utf-8',
        extra="ignore"
    )

    jwt_access_secret_key: str
    jwt_refresh_secret_key: str
    jwt_algorithm: str
    jwt_access_token_expire_minutes: int
    jwt_refresh_token_expire_days: int

