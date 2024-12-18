from fastapi.params import Depends

from src.infrastructure.repo_implementations.im_ex_repo.im_ex_repo import MongoImExRepository
from src.infrastructure.repo_implementations.order_repos.mongo_order_repository import MongoOrderRepository
from src.configs.config import config
from src.infrastructure.db.mongo import MongoDB, get_db
from src.infrastructure.repo_implementations.review_repos.mongo_review_repository import MongoReviewRepository
from src.infrastructure.repo_implementations.tool_repos.mongo_category_repository import MongoCategoryRepository
from src.infrastructure.repo_implementations.tool_repos.mongo_tool_repository import MongoToolRepository
from src.infrastructure.repo_implementations.tool_repos.mongo_type_repository import MongoTypeRepository
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


def get_mongo_tool_repo(db: AsyncIOMotorDatabase = Depends(get_db)):
    return MongoToolRepository(db, collections_config.tool_collection)


def get_mongo_type_repo(db: AsyncIOMotorDatabase = Depends(get_db)):
    return MongoTypeRepository(db, collections_config.type_collection)


def get_mongo_category_repo(db: AsyncIOMotorDatabase = Depends(get_db)):
    return MongoCategoryRepository(db, collections_config.category_collection)


def get_mongo_order_repo(db: AsyncIOMotorDatabase = Depends(get_db)):
    return MongoOrderRepository(db, collections_config.order_collection, collections_config.tool_collection,
                                collections_config.client_collection)


def get_mongo_review_repo(db: AsyncIOMotorDatabase = Depends(get_db)):
    return MongoReviewRepository(db, collections_config.review_collection)


def get_mongo_im_ex_repo(db: AsyncIOMotorDatabase = Depends(get_db)):
    return MongoImExRepository(
        db,
        collections_config.order_collection,
        collections_config.tool_collection,
        collections_config.client_collection,
        collections_config.worker_collection,
        collections_config.review_collection,
        collections_config.category_collection,
        collections_config.type_collection,
    )
