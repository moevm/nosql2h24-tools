from abc import ABC, abstractmethod
from src.core.entities.review.review import ReviewCreate, ReviewCreated, ReviewSummary, Review
from typing import List, Optional

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