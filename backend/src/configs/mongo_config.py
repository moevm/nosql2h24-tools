import os

from pydantic import Field, MongoDsn
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional
from urllib.parse import urlencode

env = os.getenv('ENV', 'dev')
config_dir = os.path.dirname(os.path.abspath(__file__))

class MongoConfig(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=os.path.join(config_dir, f"../../env/{env}/.env.{env}.db"),
        env_file_encoding='utf-8',
        extra="ignore"
    )
    mongo_user: str
    mongo_password: str
    mongo_host: str
    mongo_port: int
    mongo_db: str
    mongo_auth_db: str


    mongo_dsn: Optional[MongoDsn] = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not self.mongo_dsn:

            query_string = urlencode({"authSource": self.mongo_auth_db})

            self.mongo_dsn = MongoDsn.build(
                scheme="mongodb",
                username=self.mongo_user,
                password=self.mongo_password,
                host=self.mongo_host,
                port=self.mongo_port,
                path=self.mongo_db,
                query=query_string
            )
