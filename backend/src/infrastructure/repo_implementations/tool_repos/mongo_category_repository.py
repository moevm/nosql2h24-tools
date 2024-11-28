from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase
from pymongo.errors import PyMongoError
from src.core.entities.category.category import Category
from src.core.exceptions.server_error import DatabaseError
from src.core.repositories.tool_repos.icategory_repository import ICategoryRepository
from src.infrastructure.repo_implementations.helpers.id_mapper import str_to_objectId, objectId_to_str
from typing import List, Dict

class MongoCategoryRepository(ICategoryRepository):
    def __init__(self, db: AsyncIOMotorDatabase, category_collection: str):
        self.category_collection = db[category_collection]

    async def create(self, category: Category) -> str:
        try:
            category_dict = category.model_dump()
            result = await self.category_collection.insert_one(category_dict)
            return objectId_to_str(result.inserted_id)
        except PyMongoError:
            raise DatabaseError()

    async def delete_by_name(self, category_name: str) -> int:
        try:
            result = await self.category_collection.delete_one({"name": category_name})
            return result.deleted_count
        except PyMongoError:
            raise DatabaseError()

    async def add_to_associated_types(self, category_name: str, type_id: str) -> int:
        try:
            obj_type_id = str_to_objectId(type_id)
            result = await self.category_collection.update_one(
                {"name": category_name},
                {"$push": {"types": obj_type_id}}
            )
            return result.modified_count
        except PyMongoError:
            raise DatabaseError()

    async def delete_from_associated_types(self, category_name: str, type_id: str) -> int:
        try:
            obj_type_id = str_to_objectId(type_id)
            result = await self.category_collection.update_one(
                {"name": category_name},
                {"$pull": {"types": obj_type_id}}
            )
            return result.modified_count
        except PyMongoError:
            raise DatabaseError()

    async def exists(self, category_name: str) -> bool:
        try:
            count = await self.category_collection.count_documents({"name": category_name})
            return count > 0
        except PyMongoError:
            raise DatabaseError()

    async def is_associated_types_empty(self, category_name: str) -> bool:
        try:
            category_doc = await self.category_collection.find_one({"name": category_name})
            if category_doc:
                return len(category_doc.get("types", [])) == 0
            return True
        except PyMongoError:
            raise DatabaseError()

    async def get_all_categories(self) -> List[Dict]:
        try:
            return await self.category_collection.find().to_list(None)
        except PyMongoError:
            raise DatabaseError()