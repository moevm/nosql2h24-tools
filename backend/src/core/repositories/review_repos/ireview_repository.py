from abc import ABC, abstractmethod
from src.core.entities.review.review import ReviewCreate, ReviewCreated, ReviewSummary, Review
from typing import List, Optional
from datetime import datetime

class IReviewRepository(ABC):
    @abstractmethod
    async def create(self, review: Review) -> str:
        pass

    @abstractmethod
    async def get_reviews_by_tool_id(self, tool_id: str) -> List[Review]:
        pass

    @abstractmethod
    async def exists(self, tool_id: str, reviewer_id: str) -> bool:
        pass

    @abstractmethod
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
        pass

    @abstractmethod
    async def count_reviews(
            self,
            tool_ids: Optional[List[str]] = None,
            reviewer_ids: Optional[List[str]] = None,
            rating: Optional[int] = None,
            start_date: Optional[datetime] = None,
            end_date: Optional[datetime] = None
    ) -> int:
        pass