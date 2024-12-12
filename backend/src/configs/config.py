from pydantic_settings import BaseSettings
from src.configs.collection_config import CollectionConfig
from src.configs.jwt_config import JWTConfig
from src.configs.mongo_config import MongoConfig
from src.configs.paths import Paths
from src.configs.urls import Urls

class Config(BaseSettings):
    mongo: MongoConfig = MongoConfig()
    jwt: JWTConfig = JWTConfig()
    collections: CollectionConfig = CollectionConfig()
    paths: Paths = Paths()
    urls: Urls = Urls()

config = Config()
