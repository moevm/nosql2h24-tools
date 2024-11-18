from fastapi.params import Depends
from src.configs.config import config
from src.infrastructure.db.mongo import MongoDB, get_db
from src.infrastructure.repo_implementations.users_repos.client_repos.mongo_client_repository import \
    MongoClientRepository
from src.infrastructure.repo_implementations.users_repos.worker_repos.mongo_worker_repository import \
    MongoWorkerRepository
from motor.motor_asyncio import AsyncIOMotorDatabase
collections_config = config.collections


def get_mongo_client_repo(db: AsyncIOMotorDatabase = Depends(get_db)):
    return MongoClientRepository(db, collections_config.client_collection)

def get_mongo_worker_repo(db: AsyncIOMotorDatabase = Depends(get_db)):
    return MongoWorkerRepository(db, collections_config.worker_collection)

