from typing import Union
from src.configs.jwt_config import JWTConfig
from src.core.entities.auth.login_request import LoginRequest
from src.core.entities.users.client.client import Client
from src.core.entities.users.worker.worker import Worker
from src.core.repositories.users_repos.client_repos.iclient_repository import IClientRepository
from src.core.repositories.users_repos.worker_repos.iworker_repository import IWorkerRepository
from src.core.services.authentication.jwt.jwt_token_manager import JWTTokenManager
from src.core.utils.password_hasher.bcrypt_password_hasher import BcryptPasswordHasher


class JWTAuthentication:
    def __init__(self,
                 client_repository: IClientRepository,
                 worker_repository: IWorkerRepository,
                 jwt_config: JWTConfig):
        self.client_repository = client_repository
        self.worker_repository = worker_repository
        self.password_hasher = BcryptPasswordHasher()
        self.token_manager = JWTTokenManager(jwt_config)

    async def login(self, login_request: LoginRequest) -> Union[dict, None]:
        user = await self.authenticate(login_request)

        if not user:
            raise ValueError("Invalid email or password")

        user_data = {"sub": str(user.id), "role": "worker" if isinstance(user, Worker) else "client"}
        access_token = self.token_manager.create_access_token(payload=user_data)
        refresh_token = self.token_manager.create_refresh_token(payload=user_data)

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer"
        }

    async def authenticate(self, login_request: LoginRequest) -> Union[Client, Worker, None]:
        client = await self.client_repository.get_by_email(login_request.email)
        if client and self.password_hasher.verify_password(login_request.password, client.password):
            return client

        worker = await self.worker_repository.get_by_email(login_request.email)
        if worker and self.password_hasher.verify_password(login_request.password, worker.password):
            return worker

        return None

    def refresh_access_token(self, refresh_token: str) -> str:
        return self.token_manager.refresh_access_token(refresh_token)

