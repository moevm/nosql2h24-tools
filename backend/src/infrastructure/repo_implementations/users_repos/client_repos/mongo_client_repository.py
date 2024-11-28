from typing import Optional, List
from src.core.entities.users.client.client import Client, ClientInDB, ClientSummary
from src.core.repositories.users_repos.client_repos.iclient_repository import IClientRepository
from motor.motor_asyncio import AsyncIOMotorDatabase
from src.infrastructure.repo_implementations.helpers.id_mapper import objectId_to_str
from pymongo.errors import PyMongoError
from src.core.exceptions.server_error import DatabaseError


class MongoClientRepository(IClientRepository):
    def __init__(self, db: AsyncIOMotorDatabase, client_collection: str):
        self.client_collection = db[client_collection]

    async def get_by_email(self, email: str) -> Optional[ClientInDB]:
        try:
            client_data = await self.client_collection.find_one({'email': email})
            if client_data:
                return ClientInDB(**client_data)
            return None
        except:
            raise DatabaseError()

    async def exists(self, email: str) -> bool:
        try:
            client_data = await self.client_collection.find_one({'email': email})
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

    async def get_all_clients_summary(self) -> List[ClientSummary]:
        try:
            clients_cursor =  self.client_collection.find(
                {},
                {
                    "_id": 1, "email": 1, "name": 1, "surname": 1, "phone": 1, "image": 1
                }
            )
            clients = await clients_cursor.to_list(length=None)
            return [ClientSummary(**client) for client in clients]
        except PyMongoError:
            raise DatabaseError()

