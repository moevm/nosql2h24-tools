from src.core.exceptions.server_error import DatabaseError
from src.core.repositories.tool_repos.itool_repository import IToolRepository
from src.core.entities.tool.tool import Tool, ToolSummary, ToolDetails, ToolPages
from motor.motor_asyncio import AsyncIOMotorDatabase
from pymongo.errors import PyMongoError
from src.infrastructure.repo_implementations.helpers.id_mapper import str_to_objectId
from typing import List, Optional


class MongoToolRepository(IToolRepository):
    def __init__(self, db: AsyncIOMotorDatabase, tool_collection: str):
        self.tool_collection = db[tool_collection]

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
                    "_id": 1, "name": 1,"dailyPrice": 1, "images": 1, "rating": 1
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