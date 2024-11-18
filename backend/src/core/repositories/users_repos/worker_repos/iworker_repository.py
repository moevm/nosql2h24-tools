from abc import ABC, abstractmethod
from typing import Optional

from src.core.entities.users.worker.worker import Worker

class IWorkerRepository(ABC):
    @abstractmethod
    async def get_by_email(self, email: str) -> Optional[Worker]:
        pass

    @abstractmethod
    async def create(self, worker: Worker):
        pass