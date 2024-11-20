from pydantic_settings import BaseSettings, SettingsConfigDict



class JWTConfig(BaseSettings):
    model_config = SettingsConfigDict(
        env_file="src/.env",
        env_file_encoding='utf-8',
        extra="ignore"
    )

    jwt_access_secret_key: str
    jwt_refresh_secret_key: str
    jwt_algorithm: str
    jwt_access_token_expire_minutes: int
    jwt_refresh_token_expire_days: int

