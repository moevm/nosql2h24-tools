from src.core.entities.auth.registration_request import ClientRegistrationRequest, WorkerRegistrationRequest
from src.core.entities.users.client.client import Client
from src.core.entities.users.worker.worker import Worker
from src.core.repositories.users_repos.client_repos.iclient_repository import IClientRepository
from src.core.repositories.users_repos.worker_repos.iworker_repository import IWorkerRepository
from src.core.utils.password_hasher.bcrypt_password_hasher import BcryptPasswordHasher


class RegistrationService:
    def __init__(self, client_repo: IClientRepository, worker_repo: IWorkerRepository):
        self.client_repo = client_repo
        self.worker_repo = worker_repo
        self.password_hasher = BcryptPasswordHasher()

    async def register_client(self, registration_form: ClientRegistrationRequest):
        existing_client = await self.client_repo.get_by_email(registration_form.email)

        if existing_client:
            raise ValueError("A client with this email already exists")

        hashed_password = self.password_hasher.hash_password(password=registration_form.password)

        new_client = Client(
            email=registration_form.email,
            password=hashed_password,
            name=registration_form.name,
            surname=registration_form.surname,
        )

        created_client_id = await self.client_repo.create(new_client)

        return created_client_id

    async def register_worker(self, registration_form: WorkerRegistrationRequest):
        existing_worker = await self.worker_repo.get_by_email(registration_form.email)

        if existing_worker:
            raise ValueError("A client with this email already exists")

        hashed_password = self.password_hasher.hash_password(password=registration_form.password)

        new_worker = Worker(
            email=registration_form.email,
            password=hashed_password,
            name=registration_form.name,
            surname=registration_form.surname,
            phone=registration_form.phone,
            jobTitle=registration_form.jobTitle
        )

        created_worker_id = await self.worker_repo.create(new_worker)

        return created_worker_id