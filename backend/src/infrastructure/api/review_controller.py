from fastapi import APIRouter, Depends
from typing import List
from fastapi.security import OAuth2PasswordBearer
from src.core.entities.review.review import ReviewSummary, ReviewCreated, ReviewCreate
from src.core.services.review_service.review_service import ReviewService
from src.infrastructure.api.security.role_required import role_required, is_self
from src.infrastructure.services_instances import get_review_service

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
    path="/{tool_id}",
    status_code=200,
    response_model=List[ReviewSummary]
)
async def get_tool_reviews(
        tool_id: str,
        review_service: ReviewService = Depends(get_review_service)
):
    return await review_service.get_tool_reviews(tool_id)
