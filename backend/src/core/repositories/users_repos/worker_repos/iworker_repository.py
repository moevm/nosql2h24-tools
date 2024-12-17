from abc import ABC, abstractmethod
from typing import Optional, List

from src.core.entities.object_id_str import ObjectIdStr
from src.core.entities.users.base_user import UpdateUser, UpdatedUser, UpdatedUserPassword
from src.core.entities.users.worker.worker import Worker, WorkerInDB, WorkerPrivateSummary, WorkerPaginated


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
    async def get_random_worker(self) -> Optional[ObjectIdStr]:
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

    @abstractmethod
    async def get_paginated_workers(
            self,
            page: int,
            page_size: int,
            email: Optional[str] = None,
            name: Optional[str] = None,
            surname: Optional[str] = None,
            phone: Optional[str] = None,
            jobTitle: Optional[str] = None
    ) -> List[WorkerPaginated]:
        pass

    @abstractmethod
    async def count_workers(
            self,
            email: Optional[str] = None,
            name: Optional[str] = None,
            surname: Optional[str] = None,
            phone: Optional[str] = None,
            jobTitle: Optional[str] = None
    ) -> int:
        pass