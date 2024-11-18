from abc import ABC, abstractmethod
from typing import Optional

from src.core.entities.users.client.client import Client

class IClientRepository(ABC):
    @abstractmethod
    async def get_by_email(self, email: str) -> Optional[Client]:
        pass

    @abstractmethod
    async def create(self, client: Client) -> Client:
        pass