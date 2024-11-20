from typing import Optional, Dict, List
from src.core.entities.type.type import Type, TypeSignature
from src.core.exceptions.server_error import DatabaseError
from src.core.repositories.tool_repos.itype_repository import ITypeRepository
from src.infrastructure.repo_implementations.helpers.id_mapper import str_to_objectId, objectId_to_str
from motor.motor_asyncio import AsyncIOMotorDatabase
from pymongo.errors import PyMongoError
from bson import ObjectId

class MongoTypeRepository(ITypeRepository):
    def __init__(self, db: AsyncIOMotorDatabase, type_collection: str):
        self.type_collection = db[type_collection]

    async def create(self, type: Type) -> str:
        try:
            type_dict = type.model_dump()
            result = await self.type_collection.insert_one(type_dict)
            return objectId_to_str(result.inserted_id)
        except PyMongoError:
            raise DatabaseError()

    async def get_id_by_signature(self, type_sign: TypeSignature) -> Optional[str]:
        try:
            query = type_sign.model_dump()
            document = await self.type_collection.find_one(query, {"_id": 1})
            if document:
                return objectId_to_str(document["_id"])

            return None
        except PyMongoError:
            raise DatabaseError()

    async def delete_by_name(self, type_sign: TypeSignature) -> int:
        try:
            result = await self.type_collection.delete_one({"name": type_sign.name, "category_name": type_sign.category_name})
            return result.deleted_count
        except PyMongoError:
            raise DatabaseError()

    async def add_to_associated_tools(self, type_sign: TypeSignature, tool_id: str) -> int:
        try:
            obj_tool_id = str_to_objectId(tool_id)
            result = await self.type_collection.update_one(
                {"name": type_sign.name, "category_name": type_sign.category_name},
                {"$push": {"tools": obj_tool_id}}
            )
            return result.modified_count
        except PyMongoError:
            raise DatabaseError()

    async def delete_from_associated_tools(self, type_sign: TypeSignature, tool_id: str) -> int:
        try:
            obj_tool_id = str_to_objectId(tool_id)
            result = await self.type_collection.update_one(
                {"name": type_sign.name, "category_name": type_sign.category_name},
                {"$pull": {"tools": obj_tool_id}}
            )
            return result.modified_count
        except PyMongoError:
            raise DatabaseError()

    async def exists(self, type_sign: TypeSignature) -> bool:
        try:
            count = await self.type_collection.count_documents({"name": type_sign.name, "category_name": type_sign.category_name})
            return count > 0
        except PyMongoError:
            raise DatabaseError()

    async def is_associated_tools_empty(self, type_sign: TypeSignature) -> bool:
        try:
            type_doc = await self.type_collection.find_one({"name": type_sign.name, "category_name": type_sign.category_name})
            if type_doc:
                return len(type_doc.get("tools", [])) == 0
            return True
        except PyMongoError:
            raise DatabaseError()

    async def get_types_by_ids(self, type_ids: List[ObjectId]) -> List[Dict]:
        try:
            return await self.type_collection.find(
                {"_id": {"$in": type_ids}}
            ).to_list(None)
        except PyMongoError:
            raise DatabaseError()