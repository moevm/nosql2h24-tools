from typing import Optional
from bson import ObjectId
from src.reposiroties.text_repository import TextRepository
from motor.motor_asyncio import AsyncIOMotorDatabase
from src.schemas.text import Text, TextInDB, TextUpdate


class MongoTextRepository(TextRepository):
    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db

    async def create_text(self, text: Text) -> TextInDB:
        text_data = text.model_dump()
        result = await self.db["texts"].insert_one(text_data)
        text_data["id"] = str(result.inserted_id)
        return TextInDB(**text_data)

    async def get_text_by_id(self, text_id: str) -> Optional[TextInDB]:
        result = await self.db["texts"].find_one({"_id": ObjectId(text_id)})

        if result:
            return TextInDB.from_mongo(result)

        return None

    async def get_all_texts(self) -> list[TextInDB]:
        cursor = self.db["texts"].find()
        return [TextInDB.from_mongo(doc) async for doc in cursor]

    async def update_text(self, text: TextUpdate) -> Optional[TextInDB]:
        update_data = {"$set": text.model_dump()}
        result = await self.db["texts"].find_one_and_update(
            {"_id": ObjectId(text.id)}, update_data, return_document=True
        )

        if result:
            return TextInDB.from_mongo(result)

        return None

    async def delete_text(self, text_id: str) -> Optional[TextInDB]:
        document = await self.db["texts"].find_one({"_id": ObjectId(text_id)})

        if document:
            await self.db["texts"].delete_one({"_id": ObjectId(text_id)})
            return TextInDB.from_mongo(document)

        return None
