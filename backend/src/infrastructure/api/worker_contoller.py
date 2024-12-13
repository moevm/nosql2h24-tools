from fastapi import APIRouter, Depends
from typing import List

from src.core.entities.users.base_user import UpdatedUser, UpdateUser, UpdatedUserPassword, UpdateUserPassword
from src.core.entities.users.worker.worker import WorkerInDB, WorkerPrivateSummary
from src.core.services.worker_service.worker_service import WorkerService
from src.infrastructure.api.security.role_required import role_required
from src.infrastructure.services_instances import get_worker_service
from fastapi.security import OAuth2PasswordBearer
worker_router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

@worker_router.get(
    path="/",
    status_code=200,
    response_model=List[WorkerPrivateSummary]
)
@role_required('worker')
async def get_all_workers(
        worker_service: WorkerService = Depends(get_worker_service),
        token: str = Depends(oauth2_scheme)

):
    return await worker_service.get_all_workers_summary()


@worker_router.get(
    path="/{worker_id}/private",
    status_code=200,
    response_model=WorkerPrivateSummary
)
@role_required('self')
async def get_private_worker_summary(
        worker_id: str,
        worker_service: WorkerService = Depends(get_worker_service),
        token: str = Depends(oauth2_scheme)
):
    return worker_service.get_private_worker_summary(worker_id)


@worker_router.patch(
    path="/{worker_id}",
    status_code=200,
    response_model=UpdatedUser
)
@role_required('self')
async def update_worker(
        worker_id: str,
        data: UpdateUser,
        worker_service: WorkerService = Depends(get_worker_service),
        token: str = Depends(oauth2_scheme)
):
    return worker_service.update_worker(worker_id, data)


@worker_router.patch(
    path="/{worker_id}/password",
    status_code=200,
    response_model=UpdatedUserPassword
)
@role_required('self')
async def update_worker_password(
        worker_id: str,
        data: UpdateUserPassword,
        worker_service: WorkerService = Depends(get_worker_service),
        token: str = Depends(oauth2_scheme)
):
    return await worker_service.update_password(worker_id, data)