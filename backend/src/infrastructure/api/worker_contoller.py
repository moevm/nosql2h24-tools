from fastapi import APIRouter, Depends, Query
from typing import List, Optional
from pydantic import PositiveInt

from src.core.entities.users.base_user import UpdatedUser, UpdateUser, UpdatedUserPassword, UpdateUserPassword
from src.core.entities.users.worker.worker import WorkerPrivateSummary, WorkerPaginated, PaginatedWorkersResponse
from src.core.services.worker_service.worker_service import WorkerService
from src.infrastructure.api.security.role_required import is_worker, is_self
from src.infrastructure.services_instances import get_worker_service
from fastapi.security import OAuth2PasswordBearer


worker_router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

@worker_router.get(
    path="/paginated",
    status_code=200,
    response_model=PaginatedWorkersResponse
)
async def get_workers_paginated(
        page: PositiveInt = Query(1),
        page_size: PositiveInt = Query(12),
        email: Optional[str] = Query(None),
        name: Optional[str] = Query(None),
        surname: Optional[str] = Query(None),
        phone: Optional[str] = Query(None),
        jobTitle: Optional[str] = Query(None),
        worker_service: WorkerService = Depends(get_worker_service),
        token: str = Depends(oauth2_scheme)
):
    is_worker(token)
    return await worker_service.get_paginated_workers(
        page=page,
        page_size=page_size,
        email=email,
        name=name,
        surname=surname,
        phone=phone,
        jobTitle=jobTitle
    )


@worker_router.get(
    path="/{user_id}/private",
    status_code=200,
    response_model=WorkerPrivateSummary
)
async def get_private_worker_summary(
        user_id: str,
        worker_service: WorkerService = Depends(get_worker_service),
        token: str = Depends(oauth2_scheme)
):
    is_self(token, user_id)
    return await worker_service.get_private_worker_summary(user_id)


@worker_router.patch(
    path="/{user_id}",
    status_code=200,
    response_model=UpdatedUser
)
async def update_worker(
        user_id: str,
        data: UpdateUser,
        worker_service: WorkerService = Depends(get_worker_service),
        token: str = Depends(oauth2_scheme)
):
    is_self(token, user_id)
    return await worker_service.update_worker(user_id, data)


@worker_router.patch(
    path="/{user_id}/password",
    status_code=200,
    response_model=UpdatedUserPassword
)
async def update_worker_password(
        user_id: str,
        data: UpdateUserPassword,
        worker_service: WorkerService = Depends(get_worker_service),
        token: str = Depends(oauth2_scheme)
):
    is_self(token, user_id)
    return await worker_service.update_password(user_id, data)