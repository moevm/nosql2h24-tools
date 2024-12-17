from src.core.entities.users.base_user import UpdateUser, UpdatedUser, UpdateUserPassword, UpdatedUserPassword
from src.core.entities.users.worker.worker import WorkerInDB, WorkerPrivateSummary, WorkerPaginated, PaginatedWorkersResponse
from src.core.exceptions.client_error import ResourceNotFoundError, InvalidPasswordProvided
from src.core.repositories.users_repos.worker_repos.iworker_repository import IWorkerRepository
from typing import List, Optional
from src.configs.paths import Paths
from src.configs.urls import Urls
from src.core.utils.image_decoder.image_decoder import ImageDecoder
from src.core.utils.password_hasher.bcrypt_password_hasher import BcryptPasswordHasher


class WorkerService:
    def __init__(self, worker_repo: IWorkerRepository, paths_config: Paths, urls_config: Urls):
        self.worker_repo = worker_repo
        self.img_decoder = ImageDecoder(f"{urls_config.backend_base_url}{urls_config.api_prefix}", paths_config.client_img_storage_prefix_path)
        self.bcrypt_password_hasher = BcryptPasswordHasher()

    async def get_all_workers_summary(self) -> List[WorkerPrivateSummary]:
        return await self.worker_repo.get_all_workers_summary()

    async def update_worker(self, worker_id: str, update_data: UpdateUser) -> UpdatedUser:
        if not await self.worker_repo.exists_by_id(worker_id):
            raise ResourceNotFoundError("The client with provided id does not exist", details={"id": worker_id})
        if update_data.image:
            image_url = self.img_decoder.decode_and_save_image(update_data.image, worker_id)
            update_data.image = image_url

        return await self.worker_repo.update_worker(worker_id, update_data)

    async def update_password(self, worker_id: str, update_password: UpdateUserPassword) -> UpdatedUserPassword:
        if not await self.worker_repo.exists_by_id(worker_id):
            raise ResourceNotFoundError("The client with provided id does not exist", details={"id": worker_id})
        if not self.bcrypt_password_hasher.verify_password(update_password.current_password, await self.worker_repo.get_password_by_id(worker_id)):
            raise InvalidPasswordProvided(details={"password": update_password.current_password})

        new_hashed_password = self.bcrypt_password_hasher.hash_password(password=update_password.new_password)

        return await self.worker_repo.update_password(worker_id, new_hashed_password)

    async def get_private_worker_summary(self, worker_id: str) -> WorkerPrivateSummary:
        if not await self.worker_repo.exists_by_id(worker_id):
            raise ResourceNotFoundError("The client with provided id does not exist", details={"id": worker_id})

        return await self.worker_repo.get_private_summary_by_id(worker_id)

    async def get_paginated_workers(
            self,
            page: int,
            page_size: int,
            email: Optional[str] = None,
            name: Optional[str] = None,
            surname: Optional[str] = None,
            phone: Optional[str] = None,
            jobTitle: Optional[str] = None,
    ) -> PaginatedWorkersResponse:
        total_count = await self.worker_repo.count_workers(
            email=email,
            name=name,
            surname=surname,
            phone=phone,
            jobTitle=jobTitle
        )

        workers = await self.worker_repo.get_paginated_workers(
            page=page,
            page_size=page_size,
            email=email,
            name=name,
            surname=surname,
            phone=phone,
            jobTitle=jobTitle
        )

        return PaginatedWorkersResponse(
            workers=workers,
            totalNumber=total_count
        )