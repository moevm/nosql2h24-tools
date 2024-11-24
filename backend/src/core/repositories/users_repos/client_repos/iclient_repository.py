from abc import ABC, abstractmethod
from typing import Optional, List
from src.core.entities.users.client.client import Client, ClientInDB, ClientSummary


class IClientRepository(ABC):
    @abstractmethod
    async def get_by_email(self, email: str) -> Optional[ClientInDB]:
        pass

    @abstractmethod
    async def exists(self, email: str) -> bool:
        pass

    @abstractmethod
    async def create(self, client: Client) -> str:
        pass

    @abstractmethod
    async def get_all_clients_summary(self) -> List[ClientSummary]:
        pass