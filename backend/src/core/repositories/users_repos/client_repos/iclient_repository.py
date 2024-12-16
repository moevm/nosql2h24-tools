from abc import ABC, abstractmethod
from typing import Optional, List

from src.core.entities.users.base_user import UpdateUser, UpdatedUser, UpdateUserPassword, UpdatedUserPassword
from src.core.entities.users.client.client import Client, ClientInDB, ClientPrivateSummary, ClientFullName


class IClientRepository(ABC):
    @abstractmethod
    async def get_by_email(self, email: str) -> ClientInDB:
        pass

    @abstractmethod
    async def exists_by_email(self, email: str) -> bool:
        pass

    @abstractmethod
    async def exists_by_id(self, client_id: str) -> bool:
        pass

    @abstractmethod
    async def create(self, client: Client) -> str:
        pass

    @abstractmethod
    async def get_all_clients_summary(self) -> List[ClientPrivateSummary]:
        pass

    @abstractmethod
    async def update_client(self, client_id: str, update_client: UpdateUser) -> UpdatedUser:
        pass

    @abstractmethod
    async def get_private_summary_by_id(self, client_id: str) -> Optional[ClientPrivateSummary]:
        pass

    @abstractmethod
    async def update_password(self, client_id: str, new_password: str) -> UpdatedUserPassword:
        pass

    @abstractmethod
    async def get_password_by_id(self, client_id: str) -> str:
        pass

    @abstractmethod
    async def get_full_name(self, client_id: str) -> ClientFullName:
        pass

    @abstractmethod
    async def get_ids_by_fullname(self, name: Optional[str], surname: Optional[str]) -> List[str]:
        pass