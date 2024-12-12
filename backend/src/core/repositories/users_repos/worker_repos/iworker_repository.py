from abc import ABC, abstractmethod
from typing import Optional, List

from src.core.entities.users.base_user import UpdateUser, UpdatedUser, UpdateUserPassword, UpdatedUserPassword
from src.core.entities.users.worker.worker import Worker, WorkerInDB, WorkerPrivateSummary


class IWorkerRepository(ABC):
    @abstractmethod
    async def get_by_email(self, email: str) -> WorkerInDB:
        pass

    @abstractmethod
    async def exists_by_email(self, email: str) -> bool:
        pass

    @abstractmethod
    async def exists_by_id(self, worker_id: str) -> bool:
        pass

    @abstractmethod
    async def create(self, worker: Worker) -> str:
        pass

    @abstractmethod
    async def get_all_workers_summary(self) -> List[WorkerPrivateSummary]:
        pass

    @abstractmethod
    async def update_worker(self, worker_id: str, update_client: UpdateUser) -> UpdatedUser:
        pass

    @abstractmethod
    async def get_private_summary_by_id(self, worker_id: str) -> WorkerPrivateSummary:
        pass

    @abstractmethod
    async def update_password(self, worker_id: str, new_password: str) -> UpdatedUserPassword:
        pass

    @abstractmethod
    async def get_password_by_id(self, worker_id: str) -> str:
        pass

