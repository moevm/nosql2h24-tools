from fastapi import Depends

from src.core.services.im_ex_service.im_ex_service import ImExService
from src.core.services.order_service.order_service import OrderService
from src.core.services.review_service.review_service import ReviewService
from src.infrastructure.repo_implementations.im_ex_repo.im_ex_repo import MongoImExRepository
from src.infrastructure.repo_implementations.order_repos.mongo_order_repository import MongoOrderRepository
from src.configs.config import config
from src.core.services.authentication.jwt.jwt_auth import JWTAuthentication
from src.core.services.registration.registration import RegistrationService
from src.core.services.tool_service.tool_service import ToolService
from src.core.services.user_service.client_service import ClientService
from src.core.services.worker_service.worker_service import WorkerService
from src.infrastructure.repo_implementations.repo_instances import get_mongo_client_repo, get_mongo_order_repo, \
    get_mongo_worker_repo, \
    get_mongo_tool_repo, get_mongo_category_repo, get_mongo_type_repo, get_mongo_review_repo, get_mongo_im_ex_repo
from src.infrastructure.repo_implementations.review_repos.mongo_review_repository import MongoReviewRepository
from src.infrastructure.repo_implementations.tool_repos.mongo_category_repository import MongoCategoryRepository
from src.infrastructure.repo_implementations.tool_repos.mongo_tool_repository import MongoToolRepository
from src.infrastructure.repo_implementations.tool_repos.mongo_type_repository import MongoTypeRepository
from src.infrastructure.repo_implementations.users_repos.client_repos.mongo_client_repository import \
    MongoClientRepository
from src.infrastructure.repo_implementations.users_repos.worker_repos.mongo_worker_repository import \
    MongoWorkerRepository


def get_jwt_authenticator(
        mongo_client_repo: MongoClientRepository = Depends(get_mongo_client_repo),
        mongo_worker_repo: MongoWorkerRepository = Depends(get_mongo_worker_repo)
) -> JWTAuthentication:
    return JWTAuthentication(
        mongo_client_repo,
        mongo_worker_repo,
        config.jwt
    )


def get_registration_service(
        mongo_client_repo: MongoClientRepository = Depends(get_mongo_client_repo),
        mongo_worker_repo: MongoWorkerRepository = Depends(get_mongo_worker_repo)
) -> RegistrationService:
    return RegistrationService(
        mongo_client_repo,
        mongo_worker_repo,
    )


def get_tool_service(
        mongo_tool_repo: MongoToolRepository = Depends(get_mongo_tool_repo),
        mongo_category_repo: MongoCategoryRepository = Depends(get_mongo_category_repo),
        mongo_type_repo: MongoTypeRepository = Depends(get_mongo_type_repo)
) -> ToolService:
    return ToolService(
        mongo_tool_repo,
        mongo_category_repo,
        mongo_type_repo,
        config.paths,
        config.urls
    )


def get_client_service(
        mongo_client_repo: MongoClientRepository = Depends(get_mongo_client_repo)
) -> ClientService:
    return ClientService(
        mongo_client_repo,
        config.paths,
        config.urls
    )


def get_worker_service(
        mongo_worker_repo: MongoWorkerRepository = Depends(get_mongo_worker_repo)
) -> WorkerService:
    return WorkerService(
        mongo_worker_repo,
        config.paths,
        config.urls
    )


def get_order_service(
        mongo_order_repo: MongoOrderRepository = Depends(get_mongo_order_repo),
        mongo_tool_repo: MongoToolRepository = Depends(get_mongo_tool_repo),
        mongo_worker_repo: MongoWorkerRepository = Depends(get_mongo_worker_repo),
        mongo_client_repo: MongoClientRepository = Depends(get_mongo_client_repo)

) -> OrderService:
    return OrderService(
        mongo_order_repo,
        mongo_tool_repo,
        mongo_worker_repo,
        mongo_client_repo
    )


def get_review_service(
        mongo_review_repo: MongoReviewRepository = Depends(get_mongo_review_repo),
        mongo_tool_repo: MongoToolRepository = Depends(get_mongo_tool_repo),
        mongo_client_repo: MongoClientRepository = Depends(get_mongo_client_repo),
        mongo_order_repo: MongoOrderRepository = Depends(get_mongo_order_repo)
) -> ReviewService:
    return ReviewService(
        mongo_review_repo,
        mongo_tool_repo,
        mongo_client_repo,
        mongo_order_repo
    )


def get_im_ex_service(
        mongo_im_ex_repo: MongoImExRepository = Depends(get_mongo_im_ex_repo)
) -> ImExService:
    return ImExService(
        mongo_im_ex_repo,
    )
