from fastapi import APIRouter, Depends, Query
from typing import List, Optional
from fastapi.security import OAuth2PasswordBearer
from src.core.entities.review.review import ReviewCreated, ReviewCreate, PaginatedReviewsResponse, ReviewSummary
from src.core.services.review_service.review_service import ReviewService
from src.infrastructure.api.security.role_required import is_self, is_worker
from src.infrastructure.services_instances import get_review_service
from pydantic import PositiveInt
from datetime import datetime

review_router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

@review_router.post(
    path="/",
    status_code=201,
    response_model=ReviewCreated
)
async def create_review(
        data: ReviewCreate,
        review_service: ReviewService = Depends(get_review_service),
        token: str = Depends(oauth2_scheme)
):
    is_self(token, str(data.reviewerId))
    return await review_service.create_review(data)

@review_router.get(
    path="/paginated",
    status_code=200,
    response_model=PaginatedReviewsResponse
)
async def get_reviews_paginated(
        page: PositiveInt = Query(1),
        page_size: PositiveInt = Query(12),
        tool_name: Optional[str] = Query(None),
        reviewer_name: Optional[str] = Query(None),
        reviewer_surname: Optional[str] = Query(None),
        rating: Optional[PositiveInt] = Query(None),
        start_date: Optional[datetime] = Query(None),
        end_date: Optional[datetime] = Query(None),
        review_service: ReviewService = Depends(get_review_service),
        token: str = Depends(oauth2_scheme)
):
    is_worker(token)
    return await review_service.get_paginated_reviews(
        page=page,
        page_size=page_size,
        tool_name=tool_name,
        reviewer_name=reviewer_name,
        reviewer_surname=reviewer_surname,
        rating=rating,
        start_date=start_date,
        end_date=end_date
    )


@review_router.get(
    path="/{tool_id}",
    status_code=200,
    response_model=List[ReviewSummary]
)
async def get_tool_reviews(
        tool_id: str,
        review_service: ReviewService = Depends(get_review_service)
):
    return await review_service.get_tool_reviews(tool_id)


