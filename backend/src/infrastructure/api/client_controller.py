from fastapi import APIRouter, Depends
from typing import List
from src.core.entities.users.client.client import ClientInDB, ClientSummary
from src.core.services.user_service.client_service import ClientService
from src.infrastructure.api.security.role_required import role_required
from src.infrastructure.services_instances import get_client_service

client_router = APIRouter()

@client_router.get(
    path="/",
    status_code=200,
    response_model=List[ClientSummary]
)
async def get_all_clients(
        client_service: ClientService = Depends(get_client_service)
):
    return await client_service.get_all_clients_summary()
