from sqlite3 import DatabaseError
from src.core.entities.order.order import Order
from src.core.repositories.order_repos.iorder_repository import IOrderRepository
from motor.motor_asyncio import AsyncIOMotorDatabase
from pymongo.errors import PyMongoError


class MongoOrderRepository(IOrderRepository):
    def __init__(self, db: AsyncIOMotorDatabase, order_collection: str):
        self.order_collection = db[order_collection]
        
    async def create(self, order: Order):
        try:
            order_dict = order.model_dump()
            result = await self.order_collection.insert_one(order_dict)
            return str(result.inserted_id)
        except PyMongoError:
            raise DatabaseError()