from fastapi import Depends

from src.configs.config import config
from src.core.services.authentication.jwt.jwt_auth import JWTAuthentication
from src.core.services.registration.registration import RegistrationService
from src.infrastructure.repo_implementations.repo_instances import get_mongo_client_repo, get_mongo_worker_repo
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
