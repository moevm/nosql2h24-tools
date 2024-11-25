from unittest.mock import AsyncMock
import pytest

from src.core.entities.users.client.client import ClientSummary
from src.core.services.user_service.client_service import ClientService


@pytest.fixture
def client_repo():
    return AsyncMock()

@pytest.fixture
def client_service(client_repo):
    return ClientService(client_repo)

@pytest.fixture
def client_summaries():
    return [
        ClientSummary(
            id="1",
            email="test1@example.com",
            name="test_name_1",
            surname="test_surname_1",
            phone="+71111111111"
        ),
        ClientSummary(
            id="1",
            email="test2@example.com",
            name="test_name_2",
            surname="test_surname_2",
            phone="+72222222222"
        ),
    ]

@pytest.mark.asyncio
async def test_get_all_clients_summary_success(client_service, client_repo, client_summaries):
    client_repo.get_all_clients_summary.return_value = client_summaries

    result = await client_service.get_all_clients_summary()

    assert result == client_summaries

    client_repo.get_all_clients_summary.assert_called_once_with()