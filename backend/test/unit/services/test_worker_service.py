from datetime import datetime, timezone
from unittest.mock import AsyncMock
import pytest

from src.core.entities.users.worker.worker import WorkerSummary
from src.core.services.worker_service.worker_service import WorkerService


@pytest.fixture
def worker_repo():
    return AsyncMock()

@pytest.fixture
def worker_service(worker_repo):
    return WorkerService(worker_repo)

@pytest.fixture
def worker_summaries():
    return [
        WorkerSummary(
            id="1",
            email="test1@example.com",
            name="test_name_1",
            surname="test_surname_1",
            phone="+71111111111",
            jobTitle="test_title_1",
            date=datetime.now(timezone.utc)
        ),
        WorkerSummary(
            id="2",
            email="test2@example.com",
            name="test_name_2",
            surname="test_surname_2",
            phone="+72222222222",
            jobTitle="test_title_2",
            date=datetime.now(timezone.utc)
        )
    ]

@pytest.mark.asyncio
async def test_get_all_workers_summary_success(worker_service, worker_repo, worker_summaries):
    worker_repo.get_all_workers_summary.return_value = worker_summaries

    result = await worker_service.get_all_workers_summary()

    assert result == worker_summaries

    worker_repo.get_all_workers_summary.assert_called_once_with()