from abc import ABC, abstractmethod
from typing import Optional, List
from src.core.entities.users.worker.worker import Worker, WorkerInDB, WorkerSummary


class IWorkerRepository(ABC):
    @abstractmethod
    async def get_by_email(self, email: str) -> Optional[WorkerInDB]:
        pass

    @abstractmethod
    async def exists(self, email: str) -> bool:
        pass

    @abstractmethod
    async def create(self, worker: Worker) -> str:
        pass

    @abstractmethod
    async def get_all_workers_summary(self) -> List[WorkerSummary]:
        pass