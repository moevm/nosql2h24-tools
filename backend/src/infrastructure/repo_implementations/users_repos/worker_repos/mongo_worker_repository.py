from datetime import datetime, timezone
from typing import Optional, List
from src.core.entities.object_id_str import ObjectIdStr
from src.core.entities.users.base_user import UpdateUser, UpdatedUser, UpdatedUserPassword
from src.core.entities.users.worker.worker import Worker, WorkerInDB, WorkerPrivateSummary, WorkerPaginated
from src.core.exceptions.server_error import DatabaseError
from src.core.repositories.users_repos.worker_repos.iworker_repository import IWorkerRepository
from motor.motor_asyncio import AsyncIOMotorDatabase
from pymongo.errors import PyMongoError
from src.infrastructure.repo_implementations.helpers.id_mapper import objectId_to_str, str_to_objectId
from pymongo import ASCENDING

class MongoWorkerRepository(IWorkerRepository):
    def __init__(self, db: AsyncIOMotorDatabase, worker_collection: str):
        self.worker_collection = db[worker_collection]

    async def get_by_email(self, email: str) -> WorkerInDB:
        try:
            worker_data = await self.worker_collection.find_one({'email': email})
            return WorkerInDB(**worker_data)
        except PyMongoError:
            raise DatabaseError()

    async def exists_by_email(self, email: str) -> bool:
        try:
            worker_data = await self.worker_collection.find_one({'email': email})
            return worker_data is not None
        except PyMongoError:
            raise DatabaseError()

    async def exists_by_id(self, worker_id: str) -> bool:
        try:
            worker_data = await self.worker_collection.find_one({'_id': str_to_objectId(worker_id)})
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

    async def get_all_workers_summary(self) -> List[WorkerPrivateSummary]:
        try:
            worker_cursor = self.worker_collection.find(
                {},
                {
                    "_id": 1, "email": 1, "name": 1, "surname": 1, "phone": 1, "image": 1, "jobTitle": 1, "date": 1
                }
            )
            workers = await worker_cursor.to_list(length=None)
            return [WorkerPrivateSummary(**worker) for worker in workers]
        except PyMongoError:
            raise DatabaseError()

    async def update_worker(self, worker_id: str, update_client: UpdateUser) -> UpdatedUser:
        try:
            update_data = {key: value for key, value in update_client.model_dump(exclude_unset=True).items()}

            update_data["updated_at"] = datetime.now(timezone.utc)

            result = await self.worker_collection.update_one(
                {"_id": str_to_objectId(worker_id)},
                {"$set": update_data}
            )

            return UpdatedUser(
                user_id=worker_id
            )
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

    async def update_password(self, worker_id: str, new_password: str) -> UpdatedUserPassword:
        try:

            update_data = {
                "password": new_password,
                "updated_at": datetime.now(timezone.utc)
            }

            await self.worker_collection.update_one(
                {"_id": str_to_objectId(worker_id)},
                {"$set": update_data}
            )

            return UpdatedUserPassword(
                user_id=worker_id
            )
        except PyMongoError:
            raise DatabaseError()

    async def get_password_by_id(self, worker_id: str) -> str:
        try:
            worker_data = await self.worker_collection.find_one(
                {"_id": str_to_objectId(worker_id)},
                {"password": 1}
            )

            return worker_data["password"]
        except PyMongoError:
            raise DatabaseError()

    async def get_private_summary_by_id(self, worker_id: str) -> WorkerPrivateSummary:
        try:
            worker_data = await self.worker_collection.find_one({"_id": str_to_objectId(worker_id)})
            return WorkerPrivateSummary(**worker_data)
        except PyMongoError:
            raise DatabaseError()

    async def get_paginated_workers(
            self,
            page: int,
            page_size: int,
            email: Optional[str] = None,
            name: Optional[str] = None,
            surname: Optional[str] = None,
            phone: Optional[str] = None,
            jobTitle: Optional[str] = None
    ) -> List[WorkerPaginated]:
        try:
            skip = (page - 1) * page_size
            filters = {}

            if email:
                filters['email'] = {"$regex": email, "$options": "i"}
            if name:
                filters['name'] = {"$regex": name, "$options": "i"}
            if surname:
                filters['surname'] = {"$regex": surname, "$options": "i"}
            if phone:
                filters['phone'] = {"$regex": phone, "$options": "i"}
            if jobTitle:
                filters['jobTitle'] = {"$regex": jobTitle, "$options": "i"}

            cursor = self.worker_collection.find(
                filters,
                {
                    "_id": 1, "email": 1, "name": 1, "surname": 1, "phone": 1, "jobTitle": 1,  "date": 1
                }
            ).sort("created_at", ASCENDING).skip(skip).limit(page_size)

            workers = await cursor.to_list(length=page_size)
            return [WorkerPaginated(**worker) for worker in workers]
        except PyMongoError:
            raise DatabaseError()

    async def count_workers(
            self,
            email: Optional[str] = None,
            name: Optional[str] = None,
            surname: Optional[str] = None,
            phone: Optional[str] = None,
            jobTitle: Optional[str] = None
    ) -> int:
        try:
            filters = {}

            if email:
                filters['email'] = {"$regex": email, "$options": "i"}
            if name:
                filters['name'] = {"$regex": name, "$options": "i"}
            if surname:
                filters['surname'] = {"$regex": surname, "$options": "i"}
            if phone:
                filters['phone'] = {"$regex": phone, "$options": "i"}
            if jobTitle:
                filters['jobTitle'] = {"$regex": jobTitle, "$options": "i"}

            count = await self.worker_collection.count_documents(filters)

            return count
        except PyMongoError:
            raise DatabaseError()