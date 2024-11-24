from src.core.entities.users.worker.worker import WorkerInDB, WorkerSummary
from src.core.repositories.users_repos.worker_repos.iworker_repository import IWorkerRepository
from typing import List

class WorkerService:
    def __init__(self, worker_repo: IWorkerRepository):
        self.worker_repo = worker_repo

    async def get_all_workers_summary(self) -> List[WorkerSummary]:
        return await self.worker_repo.get_all_workers_summary()

