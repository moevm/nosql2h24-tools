from fastapi import Depends
from src.configs.config import config
from src.core.services.authentication.jwt.jwt_auth import JWTAuthentication
from src.core.services.registration.registration import RegistrationService
from src.core.services.tool_service.tool_service import ToolService
from src.core.services.user_service.client_service import ClientService
from src.core.services.worker_service.worker_service import WorkerService
from src.infrastructure.repo_implementations.repo_instances import get_mongo_client_repo, get_mongo_worker_repo, \
    get_mongo_tool_repo, get_mongo_category_repo, get_mongo_type_repo
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
        mongo_client_repo
    )

def get_worker_service(
        mongo_worker_repo: MongoWorkerRepository = Depends(get_mongo_worker_repo)
) -> WorkerService:
    return WorkerService(
        mongo_worker_repo
    )