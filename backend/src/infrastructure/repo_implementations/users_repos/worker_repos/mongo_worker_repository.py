from typing import Optional
from src.core.entities.users.worker.worker import Worker, WorkerInDB
from src.core.repositories.users_repos.worker_repos.iworker_repository import IWorkerRepository
from motor.motor_asyncio import AsyncIOMotorDatabase


class MongoWorkerRepository(IWorkerRepository):
    def __init__(self, db: AsyncIOMotorDatabase, worker_collection: str):
        self.worker_collection = db[worker_collection]

    async def get_by_email(self, email: str) -> Optional[WorkerInDB]:
        worker_data = await self.worker_collection.find_one({'email': email})
        if worker_data:
            return WorkerInDB(**worker_data)
        return None

    async def create(self, worker: Worker) -> str:
        worker_dict = worker.model_dump()
        result = await self.worker_collection.insert_one(worker_dict)
        return str(result.inserted_id)

