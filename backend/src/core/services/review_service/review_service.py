from src.core.entities.review.review import ReviewCreate, ReviewCreated, ReviewSummary, Review
from typing import List
from src.core.exceptions.client_error import ResourceNotFoundError, ResourceAlreadyExistsError, PaymentStateError
from src.core.repositories.order_repos.iorder_repository import IOrderRepository
from src.core.repositories.review_repos.ireview_repository import IReviewRepository
from src.core.repositories.tool_repos.itool_repository import IToolRepository
from src.core.repositories.users_repos.client_repos.iclient_repository import IClientRepository
from src.infrastructure.repo_implementations.helpers.id_mapper import objectId_to_str, str_to_objectId


class ReviewService:
    def __init__(self, review_repo: IReviewRepository, tool_repo: IToolRepository, client_repo: IClientRepository, order_repo: IOrderRepository):
        self.review_repo = review_repo
        self.tool_repo = tool_repo
        self.client_repo = client_repo
        self.order_repo = order_repo

    async def create_review(self, review: ReviewCreate) -> ReviewCreated:
        if not await self.tool_repo.exists_by_id(review.toolId):
            raise ResourceNotFoundError("Tool with the provided id doesn't exist")
        if not await self.client_repo.exists_by_id(review.reviewerId):
            raise ResourceNotFoundError("Client with the provided id doesn't exist")
        if not await self.order_repo.exists_by_id(review.orderId):
            raise ResourceNotFoundError("Order with the provided id doesn't exist")
        if await self.review_repo.exists(review.toolId, review.reviewerId):
            raise ResourceAlreadyExistsError("Review already exists")
        if not await self.order_repo.has_order_with_tool(review.reviewerId, review.toolId):
            raise ResourceNotFoundError("Client with provided id didn't order a tool with the provided id")
        if not await self.order_repo.paid(review.orderId):
            raise PaymentStateError("You can't leave a review, the order hasn't been paid for")

        review_id = await self.review_repo.create(
            Review(
                toolId=str_to_objectId(review.toolId),
                reviewerId=str_to_objectId(review.reviewerId),
                rating=review.rating,
                date=review.date,
                text=review.text
            )
        )


        return ReviewCreated(
            review_id=review_id
        )

    async def get_tool_reviews(self, tool_id: str) -> List[ReviewSummary]:
        if not await self.tool_repo.exists_by_id(tool_id):
            raise ResourceNotFoundError("Tool with provided id doesn't exist")

        reviews = await self.review_repo.get_reviews_by_tool_id(tool_id)
        review_summaries = []

        for review in reviews:
            client_full_name = await self.client_repo.get_full_name(objectId_to_str(review.reviewerId))

            review_summary = ReviewSummary(
                reviewer_name=client_full_name.name,
                reviewer_surname=client_full_name.surname,
                rating=review.rating,
                date=review.date,
                text=review.text
            )
            review_summaries.append(review_summary)

        return review_summaries