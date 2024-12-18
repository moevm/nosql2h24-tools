from src.core.exceptions.server_error import DatabaseError
from src.core.repositories.tool_repos.itool_repository import IToolRepository
from src.core.entities.tool.tool import Tool, ToolSummary, ToolDetails, ToolPages
from motor.motor_asyncio import AsyncIOMotorDatabase
from pymongo.errors import PyMongoError
from src.infrastructure.repo_implementations.helpers.id_mapper import str_to_objectId, objectId_to_str
from typing import List, Optional


class MongoToolRepository(IToolRepository):
    def __init__(self, db: AsyncIOMotorDatabase, tool_collection: str):
        self.tool_collection = db[tool_collection]
        self.tool_collection_name = tool_collection

    async def create(self, tool: Tool) -> str:
        try:
            tool_dict = tool.model_dump()
            result = await self.tool_collection.insert_one(tool_dict)
            return str(result.inserted_id)
        except PyMongoError:
            raise DatabaseError()

    async def get_paginated_summary(self, page: int, page_size: int) -> List[ToolSummary]:
        try:
            skip = (page - 1) * page_size
            tools = await self.tool_collection.find(
                {},
                {
                    "_id": 1, "name": 1,"dailyPrice": 1, "images": 1, "rating": 1, "description": 1
                }
            ).skip(skip).limit(page_size).to_list(length=page_size)
            tool_models = [ToolSummary(**tool) for tool in tools]
            return tool_models
        except PyMongoError:
            raise DatabaseError()

    async def get_details(self, tool_id: str) -> Optional[ToolDetails]:
        try:
            obj_tool_id = str_to_objectId(tool_id)
            tool = await self.tool_collection.find_one(
                {"_id": obj_tool_id},
                {
                    "_id": 1, "name": 1, "dailyPrice": 1, "images": 1, "features": 1, "rating": 1, "category": 1, "type": 1, "description": 1
                }
            )

            if not tool:
                return None

            tool_details = ToolDetails(**tool)
            return tool_details
        except PyMongoError:
            raise DatabaseError()


    async def get_total_count(self) -> ToolPages:
        try:
            total_count = await self.tool_collection.count_documents({})
            return ToolPages(pages=total_count)
        except PyMongoError:
            raise DatabaseError()


    async def exists(self, tool_name: str) -> bool:
        try:
            count = await self.tool_collection.count_documents({"name": tool_name})
            return count > 0
        except PyMongoError:
            raise DatabaseError()

    async def get_tool_by_id(self, tool_id: str) -> Optional[Tool]:
        try:
            obj_tool_id = str_to_objectId(tool_id)
            tool = await self.tool_collection.find_one(
                {"_id": obj_tool_id},
                {
                    "_id": 1, "name": 1, "dailyPrice": 1, "images": 1, "features": 1, "rating": 1, "category": 1,
                    "type": 1, "description": 1
                }
            )
            if not tool:
                return None
            return Tool(**tool)
        except PyMongoError:
            raise DatabaseError()

    async def search(
            self,
            query: str,
            page: int,
            page_size: int,
            category: Optional[List[str]] = None,
            type: Optional[List[str]] = None,
            min_price: Optional[float] = None,
            max_price: Optional[float] = None
    ) -> List[ToolSummary]:
        try:
            skip = (page - 1) * page_size

            match_stage = {"$match": {"$text": {"$search": query}}}

            if category:
                match_stage["$match"]["category"] = {"$in": category}
            if type:
                match_stage["$match"]["type"] = {"$in": type}
            if min_price is not None:
                match_stage["$match"]["dailyPrice"] = {"$gte": min_price}
            if max_price is not None:
                match_stage["$match"].setdefault("dailyPrice", {})["$lte"] = max_price


            pipeline = [
                match_stage,
                {"$addFields": {"score": {"$meta": "textScore"}}},
                {"$sort": {"score": -1, "_id": 1}},
                {"$skip": skip},
                {"$limit": page_size},
                {"$project": {
                    "_id": 1,
                    "name": 1,
                    "dailyPrice": 1,
                    "images": 1,
                    "rating": 1,
                    "description": 1,
                }}
            ]
            cursor = self.tool_collection.aggregate(pipeline)

            results = []

            async for doc in cursor:
                results.append(ToolSummary(**doc))

            return results
        except PyMongoError:
            raise DatabaseError()

    async def exists_by_id(self, tool_id: str) -> bool:
        try:
            tool = await self.tool_collection.find_one({'_id': str_to_objectId(tool_id)})
            return tool is not None
        except PyMongoError:
            raise DatabaseError()

    async def get_name_by_id(self, tool_id: str) -> Optional[str]:
        try:
            tool_data = await self.tool_collection.find_one(
                {"_id": str_to_objectId(tool_id)},
                {"_id": 0, "name": 1}
            )

            if tool_data:
                return tool_data["name"]
            return None
        except PyMongoError as e:
            raise DatabaseError()

    async def get_ids_by_name(self, name: str) -> List[str]:
        try:
            cursor = self.tool_collection.find(
                {"name": {"$regex": name, "$options": "i"}},
                {"_id": 1}
            )

            tools = await cursor.to_list(length=None)
            return [objectId_to_str(tool["_id"]) for tool in tools]

        except PyMongoError:
            raise DatabaseError()

    async def get_ids_by_names(self, names: List[str]) -> List[str]:
        try:
            regex_filters = [{"name": {"$regex": name, "$options": "i"}} for name in names]
            cursor = self.tool_collection.find(
                {"$or": regex_filters},
                {"_id": 1}
            )

            tools = await cursor.to_list(length=None)
            return [objectId_to_str(tool["_id"]) for tool in tools]
        except PyMongoError:
            raise DatabaseError()

    async def count_tools(
            self,
            query: str,
            category: Optional[List[str]] = None,
            type: Optional[List[str]] = None,
            min_price: Optional[float] = None,
            max_price: Optional[float] = None
    ) -> int:
        try:
            filters = {"$text": {"$search": query}}

            if category:
                filters["category"] = {"$in": category}
            if type:
                filters["type"] = {"$in": type}
            if min_price is not None:
                filters["dailyPrice"] = {"$gte": min_price}
            if max_price is not None:
                filters.setdefault("dailyPrice", {})["$lte"] = max_price

            return await self.tool_collection.count_documents(filters)

        except PyMongoError:
            raise DatabaseError()

    async def get_tools_summaries_by_ids(self, tool_ids: List[str]) -> List[ToolSummary]:
        try:
            cursor = self.tool_collection.find(
                {"_id": {"$in": [str_to_objectId(tool_id) for tool_id in tool_ids]}},
                {"_id": 1, "name": 1, "dailyPrice": 1, "images": 1, "rating": 1, "description": 1}
            )

            results = []

            async for doc in cursor:
                results.append(ToolSummary(**doc))

            return results
        except PyMongoError:
            raise DatabaseError()

    async def update_rating(self, tool_id: str, new_rating: float) -> None:
        try:
            tool_data = await self.tool_collection.find_one({"_id": str_to_objectId(tool_id)}, {"rating": 1, "reviews_count": 1})

            updated_reviews_count = tool_data["reviews_count"] + 1
            updated_rating = (tool_data["rating"] * tool_data["reviews_count"] + new_rating) / updated_reviews_count

            await self.tool_collection.update_one(
                {"_id": str_to_objectId(tool_id)},
                {"$set": {"rating": updated_rating, "reviews_count": updated_reviews_count}}
            )
        except PyMongoError:
            raise DatabaseError()