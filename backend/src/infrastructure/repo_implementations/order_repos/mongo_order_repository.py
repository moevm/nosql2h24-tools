from datetime import datetime
from sqlite3 import DatabaseError
from typing import Optional, List

from src.core.entities.order.order import Order, OrderSummary, OrderForWorker, OrderInDB
from src.core.entities.tool.tool import ToolSummary
from src.core.entities.users.client.client import ClientForWorker
from src.core.repositories.order_repos.iorder_repository import IOrderRepository
from motor.motor_asyncio import AsyncIOMotorDatabase
from pymongo.errors import PyMongoError

from src.infrastructure.repo_implementations.helpers.id_mapper import str_to_objectId, objectId_to_str


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


    async def get_order_by_id(self, order_id: str) -> Optional[OrderSummary]:
        try:
            obj_id = str_to_objectId(order_id)
            order = await self.order_collection.find_one({"_id": obj_id})
            if not order:
                return None
            tools_id = order.get("tools", [])
            tools = await self.tool_collection.find(
                {"_id": {"$in": tools_id}},
                {"_id": 1, "name": 1, "dailyPrice": 1, "images": 1, "features": 1, "rating": 1, "category": 1,
                 "type": 1, "description": 1}
            ).to_list(length=None)
            tools_model = [ToolSummary(**tool) for tool in tools]
            print(order)
            return OrderSummary(
                id=objectId_to_str(order["_id"]),
                price=order["price"],
                tools=tools,
                start_leasing=order["start_leasing"],
                end_leasing=order["end_leasing"],
                delivery_type=order["delivery_type"],
                delivery_state=order["delivery_state"],
                payment_type=order["payment_type"],
                payment_state=order["payment_state"],
                create_order_time=order["create_order_time"]
            )
        except PyMongoError:
            raise DatabaseError()

    async def has_order_with_tool(self, client_id: str, tool_id: str) -> bool:
        try:
            result = await self.order_collection.find_one(
                {
                    "client": str_to_objectId(client_id),
                    "tools": str_to_objectId(tool_id)
                },
                {
                    "_id": 1
                }
            )

            return result is not None
        except PyMongoError:
            raise DatabaseError()

    async def paid(self, order_id: str) -> bool:
        try:
            result = await self.order_collection.find_one(
                {
                    "_id": str_to_objectId(order_id),
                    "payment_state": "paid"
                },
                {
                    "_id": 1
                }
            )

            return result is not None
        except PyMongoError:
            raise DatabaseError()

    async def exists_by_id(self, order_id: str) -> bool:
        try:
            order = await self.order_collection.find_one({'_id': str_to_objectId(order_id)})
            return order is not None
        except PyMongoError:
            raise DatabaseError()

    async def get_paginated_orders(
            self,
            page: int,
            page_size: int,
            customer_ids: Optional[List[str]] = None,
            tool_ids: Optional[List[str]] = None,
            status: Optional[str] = None,
            start_date: Optional[datetime] = None,
            end_date: Optional[datetime] = None,
            min_price: Optional[float] = None,
            max_price: Optional[float] = None
    ) -> List[OrderInDB]:
        try:
            skip = (page - 1) * page_size
            filters = {}
            print(max_price)
            if min_price is not None:
                filters["price"] = {"$gte": min_price}
            if max_price is not None:
                filters.setdefault("price", {})["$lte"] = max_price


            if start_date or end_date:
                filters["create_order_time"] = {}
            if start_date:
                filters["create_order_time"]["$gte"] = start_date
            if end_date:
                filters["create_order_time"]["$lte"] = end_date

            if status:
                filters["delivery_state"] = {"$regex": status, "$options": "i"}

            if tool_ids is not None:
                filters["tools"] = {"$in": [str_to_objectId(tool_id) for tool_id in tool_ids]}

            if customer_ids is not None:
                filters["client"] = {"$in": [str_to_objectId(customer_id) for customer_id in customer_ids]}

            cursor = self.order_collection.find(filters).skip(skip).limit(page_size)
            orders = await cursor.to_list(length=page_size)
            print(filters)

            return [OrderInDB(**doc) for doc in orders]
        except PyMongoError:
            raise DatabaseError()

    async def count_orders(
            self,
            customer_ids: Optional[List[str]] = None,
            tool_ids: Optional[List[str]] = None,
            status: Optional[str] = None,
            start_date: Optional[datetime] = None,
            end_date: Optional[datetime] = None,
            min_price: Optional[float] = None,
            max_price: Optional[float] = None
    ) -> int:
        try:
            filters = {}

            if min_price is not None:
                filters["price"] = {"$gte": min_price}
            if max_price is not None:
                filters.setdefault("price", {})["$lte"] = max_price


            if start_date or end_date:
                filters["create_order_time"] = {}
            if start_date:
                filters["create_order_time"]["$gte"] = start_date
            if end_date:
                filters["create_order_time"]["$lte"] = end_date

            if status:
                filters["delivery_state"] = {"$regex": status, "$options": "i"}

            if tool_ids is not None:
                filters["tools"] = {"$in": [str_to_objectId(tool_id) for tool_id in tool_ids]}

            if customer_ids is not None:
                filters["client"] = {"$in": [str_to_objectId(customer_id) for customer_id in customer_ids]}

            return await self.order_collection.count_documents(filters)
        except PyMongoError:
            raise DatabaseError()