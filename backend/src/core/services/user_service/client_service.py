from src.core.entities.users.client.client import ClientInDB, ClientSummary
from src.core.repositories.users_repos.client_repos.iclient_repository import IClientRepository
from typing import List

class ClientService:
    def __init__(self, client_repo: IClientRepository):
        self.client_repo = client_repo

    async def get_all_clients_summary(self) -> List[ClientSummary]:
        return await self.client_repo.get_all_clients_summary()
