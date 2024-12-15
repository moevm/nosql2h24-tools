from src.core.entities.review.review import ReviewCreate, Review
from src.core.repositories.review_repos.ireview_repository import IReviewRepository
from motor.motor_asyncio import AsyncIOMotorDatabase
from src.core.exceptions.server_error import DatabaseError
from pymongo.errors import PyMongoError
from typing import List
from src.infrastructure.repo_implementations.helpers.id_mapper import str_to_objectId


class MongoReviewRepository(IReviewRepository):
    def __init__(self, db: AsyncIOMotorDatabase, review_collection: str):
        self.review_collection = db[review_collection]

    async def create(self, review: Review) -> str:
        try:
            review_dict = review.model_dump()
            result = await self.review_collection.insert_one(review_dict)
            return str(result.inserted_id)
        except PyMongoError:
            raise DatabaseError()

    async def get_reviews_by_tool_id(self, tool_id: str) -> List[Review]:
        try:
            cursor = self.review_collection.find({"toolId": str_to_objectId(tool_id)})
            reviews = await cursor.to_list(length=None)
            return [Review(**review) for review in reviews]
        except PyMongoError:
            raise DatabaseError()


    async def exists(self, tool_id: str, reviewer_id: str) -> bool:
        try:
            result = await self.review_collection.find_one(
                {
                    "toolId": str_to_objectId(tool_id),
                    "reviewerId": str_to_objectId(reviewer_id)
                },
                {"_id": 1}
            )

            return result is not None
        except PyMongoError:
            raise DatabaseError()

