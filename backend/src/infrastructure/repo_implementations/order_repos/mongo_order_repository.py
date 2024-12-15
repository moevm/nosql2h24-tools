from sqlite3 import DatabaseError
from typing import Optional, List

from src.core.entities.order.order import Order, OrderSummary, OrderForWorker
from src.core.entities.tool.tool import ToolSummary
from src.core.entities.users.client.client import ClientForWorker
from src.core.repositories.order_repos.iorder_repository import IOrderRepository
from motor.motor_asyncio import AsyncIOMotorDatabase
from pymongo.errors import PyMongoError

from src.infrastructure.repo_implementations.helpers.id_mapper import str_to_objectId


class MongoOrderRepository(IOrderRepository):
    def __init__(self, db: AsyncIOMotorDatabase, order_collection: str, tool_collection: str, client_collection: str):
        self.order_collection = db[order_collection]
        self.tool_collection = db[tool_collection]
        self.client_collection = db[client_collection]

    async def create(self, order: Order):
        try:
            order_dict = order.model_dump()
            result = await self.order_collection.insert_one(order_dict)
            return str(result.inserted_id)
        except PyMongoError:
            raise DatabaseError()

    async def get_orders_by_client_id(self, client_id: str) -> Optional[List[OrderSummary]]:
        try:
            obj_client_id = str_to_objectId(client_id)
            orders_cursor = self.order_collection.find(
                {"client": obj_client_id},
                {"_id": 1, "tools": 1, "start_leasing": 1, "end_leasing": 1, "delivery_type": 1, "delivery_state": 1,
                 "payment_type": 1, "payment_state": 1},
            )
            orders = await orders_cursor.to_list(length=None)
            for order in orders:
                tool_ids = order.get("tools", [])
                tools = await self.tool_collection.find(
                    {"_id": {"$in": tool_ids}},
                    {"_id": 1, "name": 1, "dailyPrice": 1, "images": 1, "features": 1, "rating": 1, "category": 1,
                     "type": 1, "description": 1}
                ).to_list(length=None)
                tools_model = [ToolSummary(**tool) for tool in tools]
                order["tools"] = tools_model
            if not orders:
                return None
            return [OrderSummary(**order) for order in orders]
        except PyMongoError:
            raise DatabaseError()

    async def get_orders_by_worker_id(self, worker_id: str) -> Optional[List[OrderForWorker]]:
        try:
            obj_id = str_to_objectId(worker_id)
            orders_cursor = self.order_collection.find(
                {"related_worker": obj_id},
                {"_id": 1, "tools": 1, "start_leasing": 1, "price": 1, "end_leasing": 1, "client": 1,
                 "delivery_type": 1, "delivery_state": 1,
                 "payment_type": 1, "payment_state": 1, "create_order_time": 1},

            )
            orders = await orders_cursor.to_list(length=None)
            for order in orders:
                tool_ids = order.get("tools", [])
                tools = await self.tool_collection.find(
                    {"_id": {"$in": tool_ids}},
                    {"_id": 1, "name": 1, "dailyPrice": 1, "images": 1, "features": 1, "rating": 1, "category": 1,
                     "type": 1, "description": 1}
                ).to_list(length=None)
                tools_model = [ToolSummary(**tool) for tool in tools]
                order["tools"] = tools_model
                client_id = order["client"]
                client = await self.client_collection.find_one(
                    {"_id": client_id},
                    {"_id": 1, "name": 1, "surname": 1}
                )
                client_model = ClientForWorker(**client)
                order["client"] = client_model
            if not orders:
                return None
            print(orders[0])
            return [OrderForWorker(**order) for order in orders]
        except PyMongoError:
            raise DatabaseError()

    async def get_order_by_id(self, order_id: str) -> Optional[Order]:
        try:
            obj_id = str_to_objectId(order_id)
            order = await self.order_collection.find_one({"_id": obj_id})
            if not order:
                return None
            print(order)
            return Order(**order)
        except PyMongoError:
            raise DatabaseError()
