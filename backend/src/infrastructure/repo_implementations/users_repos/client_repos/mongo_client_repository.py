from typing import Optional

from src.core.entities.users.client.client import Client, ClientInDB
from src.core.repositories.users_repos.client_repos.iclient_repository import IClientRepository
from motor.motor_asyncio import AsyncIOMotorDatabase

class MongoClientRepository(IClientRepository):
    def __init__(self, db: AsyncIOMotorDatabase, client_collection: str):
        self.client_collection = db[client_collection]

    async def get_by_email(self, email: str) -> Optional[ClientInDB]:
        client_data = await self.client_collection.find_one({'email': email})
        print(client_data)
        if client_data:
            return ClientInDB(**client_data)
        return None

    async def create(self, client: Client) -> str:
        client_dict = client.model_dump()
        result = await self.client_collection.insert_one(client_dict)
        return str(result.inserted_id)

