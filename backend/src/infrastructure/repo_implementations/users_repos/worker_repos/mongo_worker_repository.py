from typing import Optional
from src.core.entities.users.worker.worker import Worker, WorkerInDB
from src.core.exceptions.server_error import DatabaseError
from src.core.repositories.users_repos.worker_repos.iworker_repository import IWorkerRepository
from motor.motor_asyncio import AsyncIOMotorDatabase
from pymongo.errors import PyMongoError
from src.infrastructure.repo_implementations.helpers.id_mapper import objectId_to_str


class MongoWorkerRepository(IWorkerRepository):
    def __init__(self, db: AsyncIOMotorDatabase, worker_collection: str):
        self.worker_collection = db[worker_collection]

    async def get_by_email(self, email: str) -> Optional[WorkerInDB]:
        try:
            worker_data = await self.worker_collection.find_one({'email': email})
            if worker_data:
                return WorkerInDB(**worker_data)
            return None
        except PyMongoError:
            raise DatabaseError()

    async def exists(self, email: str) -> bool:
        try:
            worker_data = await self.worker_collection.find_one({'email': email})
            return worker_data is not None
        except PyMongoError:
            raise DatabaseError()

    async def create(self, worker: Worker) -> str:
        try:
            worker_dict = worker.model_dump()
            result = await self.worker_collection.insert_one(worker_dict)
            return objectId_to_str(result.inserted_id)
        except PyMongoError:
            raise DatabaseError()

