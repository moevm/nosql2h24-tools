from fastapi import APIRouter, Depends
from typing import List
from src.core.entities.users.worker.worker import WorkerInDB, WorkerSummary
from src.core.services.worker_service.worker_service import WorkerService
from src.infrastructure.api.security.role_required import role_required
from src.infrastructure.services_instances import get_worker_service
from fastapi.security import OAuth2PasswordBearer
worker_router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

@worker_router.get(
    path="/",
    status_code=200,
    response_model=List[WorkerSummary]
)
@role_required('worker')
async def get_all_workers(
        worker_service: WorkerService = Depends(get_worker_service),
        token: str = Depends(oauth2_scheme)

):
    return await worker_service.get_all_workers_summary()