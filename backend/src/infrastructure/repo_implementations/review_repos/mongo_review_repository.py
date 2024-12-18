from unittest import skipIf

from src.core.entities.review.review import ReviewCreate, Review
from src.core.repositories.review_repos.ireview_repository import IReviewRepository
from motor.motor_asyncio import AsyncIOMotorDatabase
from src.core.exceptions.server_error import DatabaseError
from pymongo.errors import PyMongoError
from typing import List, Optional
from src.infrastructure.repo_implementations.helpers.id_mapper import str_to_objectId
from datetime import datetime

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

    async def get_paginated_reviews(
            self,
            page: int,
            page_size: int,
            tool_ids: Optional[List[str]] = None,
            reviewer_ids: Optional[List[str]] = None,
            rating: Optional[int] = None,
            start_date: Optional[datetime] = None,
            end_date: Optional[datetime] = None
    ) -> List[Review]:
        try:
            skip = (page - 1) * page_size
            filters = {}


            if tool_ids is not None:
                filters["toolId"] = {"$in": [str_to_objectId(tool_id) for tool_id in tool_ids]}
            if reviewer_ids is not None:
                filters["reviewerId"] = {"$in": [str_to_objectId(reviewer_id) for reviewer_id in reviewer_ids]}
            if rating is not None:
                filters["rating"] = rating
            if start_date or end_date:
                filters["date"] = {}
                if start_date:
                    filters["date"]["$gte"] = start_date
                if end_date:
                    filters["date"]["$lte"] = end_date

            cursor = self.review_collection.find(
                filters,
                {
                    "_id": 0,
                    "reviewerId": 1,
                    "toolId": 1,
                    "rating": 1,
                    "date": 1,
                    "text": 1
                }
            ).sort("date", -1).skip(skip).limit(page_size)

            reviews = await cursor.to_list(length=page_size)

            return [Review(**review) for review in reviews]
        except PyMongoError:
            raise DatabaseError()


    async def count_reviews(
            self,
            tool_ids: Optional[List[str]] = None,
            reviewer_ids: Optional[List[str]] = None,
            rating: Optional[int] = None,
            start_date: Optional[datetime] = None,
            end_date: Optional[datetime] = None
    ) -> int:
        try:
            filters = {}

            if tool_ids is not None:
                filters["toolId"] = {"$in": [str_to_objectId(tool_id) for tool_id in tool_ids]}
            if reviewer_ids is not None:
                filters["reviewerId"] = {"$in": [str_to_objectId(reviewer_id) for reviewer_id in reviewer_ids]}
            if rating is not None:
                filters["rating"] = rating
            if start_date or end_date:
                filters["date"] = {}
                if start_date:
                    filters["date"]["$gte"] = start_date
                if end_date:
                    filters["date"]["$lte"] = end_date

            count = await self.review_collection.count_documents(filters)

            return count
        except PyMongoError:
            raise DatabaseError()