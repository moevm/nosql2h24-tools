from typing import Optional, List

from src.core.entities.object_id_str import ObjectIdStr
from src.core.entities.users.worker.worker import Worker, WorkerInDB, WorkerSummary
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

    async def get_all_workers_summary(self) -> List[WorkerSummary]:
        try:
            worker_cursor = self.worker_collection.find(
                {},
                {
                    "_id": 1, "email": 1, "name": 1, "surname": 1, "phone": 1, "image": 1, "jobTitle": 1, "date": 1
                }
            )
            workers = await worker_cursor.to_list(length=None)
            return [WorkerSummary(**worker) for worker in workers]
        except PyMongoError:
            raise DatabaseError()
        
    async def get_random_worker(self) -> Optional[ObjectIdStr]:
        try:
            pipeline = [{"$sample": {"size": 1}}]
            worker_data = await self.worker_collection.aggregate(pipeline).to_list(length=1)
            if worker_data:
                return WorkerInDB(**worker_data[0]).id
            return None
        except PyMongoError:
            raise DatabaseError()
