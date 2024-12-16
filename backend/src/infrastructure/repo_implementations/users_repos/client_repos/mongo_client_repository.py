from datetime import datetime, timezone
from typing import Optional, List
from src.core.entities.object_id_str import ObjectIdStr
from src.core.entities.users.base_user import UpdateUser, UpdatedUser, UpdateUserPassword, UpdatedUserPassword
from src.core.entities.users.client.client import Client, ClientInDB, ClientPrivateSummary, ClientFullName
from src.core.repositories.users_repos.client_repos.iclient_repository import IClientRepository
from motor.motor_asyncio import AsyncIOMotorDatabase
from src.infrastructure.repo_implementations.helpers.id_mapper import objectId_to_str, str_to_objectId
from pymongo.errors import PyMongoError
from src.core.exceptions.server_error import DatabaseError


class MongoClientRepository(IClientRepository):
    def __init__(self, db: AsyncIOMotorDatabase, client_collection: str):
        self.client_collection = db[client_collection]

    async def get_by_email(self, email: str) -> ClientInDB:
        try:
            client_data = await self.client_collection.find_one({'email': email})
            return ClientInDB(**client_data)
        except:
            raise DatabaseError()

    async def exists_by_email(self, email: str) -> bool:
        try:
            client_data = await self.client_collection.find_one({'email': email})
            return client_data is not None
        except PyMongoError:
            raise DatabaseError()

    async def get_full_name(self, client_id: str) -> ClientFullName:
        try:
            client = await self.client_collection.find_one({"_id": str_to_objectId(client_id)}, {"name": 1, "surname": 1})

            return ClientFullName(
                name=client["name"],
                surname=client["surname"]
            )
        except PyMongoError:
            raise DatabaseError()

    async def exists_by_id(self, client_id: str) -> bool:
        try:
            client_data = await self.client_collection.find_one({'_id': str_to_objectId(client_id)})
            return client_data is not None
        except PyMongoError:
            raise DatabaseError()

    async def create(self, client: Client) -> str:
        try:
            client_dict = client.model_dump()
            result = await self.client_collection.insert_one(client_dict)
            return objectId_to_str(result.inserted_id)
        except PyMongoError:
            raise DatabaseError()

    async def get_all_clients_summary(self) -> List[ClientPrivateSummary]:
        try:
            clients_cursor =  self.client_collection.find(
                {},
                {
                    "_id": 1, "email": 1, "name": 1, "surname": 1, "phone": 1, "image": 1
                }
            )
            clients = await clients_cursor.to_list(length=None)
            return [ClientPrivateSummary(**client) for client in clients]
        except PyMongoError:
            raise DatabaseError()

    async def update_client(self, client_id: str, update_client: UpdateUser) -> UpdatedUser:
        try:
            update_data = {key: value for key, value in update_client.model_dump(exclude_unset=True).items()}

            update_data["updated_at"] = datetime.now(timezone.utc)

            result = await self.client_collection.update_one(
                {"_id": str_to_objectId(client_id)},
                {"$set": update_data}
            )

            return UpdatedUser(
                user_id=client_id
            )
        except PyMongoError:
            raise DatabaseError()

    async def update_password(self, client_id: str, new_password: str) -> UpdatedUserPassword:
        try:

            update_data = {
                "password": new_password,
                "updated_at": datetime.now(timezone.utc)
            }

            await self.client_collection.update_one(
                {"_id": str_to_objectId(client_id)},
                {"$set": update_data}
            )

            return UpdatedUserPassword(
                user_id=client_id
            )
        except PyMongoError:
            raise DatabaseError()

    async def get_password_by_id(self, client_id: str) -> str:
        try:
            client_data = await self.client_collection.find_one(
                {"_id": str_to_objectId(client_id)},
                {"password": 1}
            )

            return client_data["password"]
        except PyMongoError:
            raise DatabaseError()

    async def get_private_summary_by_id(self, client_id: str) -> ClientPrivateSummary:
        try:
            client_data = await self.client_collection.find_one({"_id": str_to_objectId(client_id)})
            return ClientPrivateSummary(**client_data)
        except:
            raise DatabaseError()

    async def get_ids_by_fullname(self, name: Optional[str], surname: Optional[str]) -> List[str]:
        try:
            filters = {}
            if name:
                filters["name"] = {"$regex": name, "$options": "i"}
            if surname:
                filters["surname"] = {"$regex": surname, "$options": "i"}

            cursor = self.client_collection.find(
                filters,
                {"_id": 1}
            )
            clients = await cursor.to_list(length=None)

            return [objectId_to_str(client["_id"]) for client in clients]
        except PyMongoError:
            raise DatabaseError()