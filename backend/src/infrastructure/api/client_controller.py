from fastapi import APIRouter, Depends
from typing import List

from src.core.entities.users.base_user import UpdatedUser, UpdateUser, UpdatedUserPassword, UpdateUserPassword
from src.core.entities.users.client.client import ClientInDB, ClientPrivateSummary
from src.core.services.user_service.client_service import ClientService
from src.infrastructure.api.security.role_required import role_required
from src.infrastructure.services_instances import get_client_service
from fastapi.security import OAuth2PasswordBearer

client_router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

@client_router.get(
    path="/",
    status_code=200,
    response_model=List[ClientPrivateSummary]
)
@role_required('worker')
async def get_all_clients(
        client_service: ClientService = Depends(get_client_service),
        token: str = Depends(oauth2_scheme)
):
    return await client_service.get_all_clients_summary()


@client_router.get(
    path="/{user_id}/private",
    status_code=200,
    response_model=ClientPrivateSummary
)
@role_required('self')
async def get_private_client_summary(
        user_id: str,
        client_service: ClientService = Depends(get_client_service),
        token: str = Depends(oauth2_scheme)
):
    return await client_service.get_private_client_summary(user_id)


@client_router.patch(
    path="/{user_id}",
    status_code=200,
    response_model=UpdatedUser
)
@role_required('self')
async def update_client(
        user_id: str,
        data: UpdateUser,
        client_service: ClientService = Depends(get_client_service),
        token: str = Depends(oauth2_scheme)
):
    return await client_service.update_client(user_id, data)


@client_router.patch(
    path="/{user_id}/password",
    status_code=200,
    response_model=UpdatedUserPassword
)
@role_required('self')
async def update_client_password(
        user_id: str,
        data: UpdateUserPassword,
        client_service: ClientService = Depends(get_client_service),
        token: str = Depends(oauth2_scheme)
):
    return await client_service.update_password(user_id, data)