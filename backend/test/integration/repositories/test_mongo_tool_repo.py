from unittest.mock import AsyncMock

import pytest_asyncio, pytest
from src.configs.config import config
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
from src.core.entities.tool.tool import Tool, ToolCreate, ToolSummary, ToolDetails, ToolPages
from src.core.exceptions.server_error import DatabaseError
from src.infrastructure.repo_implementations.helpers.id_mapper import objectId_to_str
from src.infrastructure.repo_implementations.tool_repos.mongo_tool_repository import MongoToolRepository
from pymongo.errors import PyMongoError


@pytest_asyncio.fixture(scope='function')
async def db():
    client = AsyncIOMotorClient(str(config.mongo.mongo_dsn))
    database = client[config.mongo.mongo_db]

    await database.drop_collection(config.collections.tool_collection)

    yield database

    await database.drop_collection(config.collections.tool_collection)

@pytest_asyncio.fixture(scope='function')
async def tool_repo(db):
    return MongoToolRepository(db, config.collections.tool_collection)

@pytest.fixture
def tool():
    return Tool(
        name="test_tool",
        dailyPrice=10.0,
        totalPrice=100.0,
        images=["image1.png", "image2.png"],
        features={"feature1": "value1", "feature2": "value2"},
        reviews=[],
        rating=4.5,
        ordersNumber=10,
        category="test_category",
        type="test_type",
        description="test_description"
    )

@pytest.fixture
def tool_create():
    return ToolCreate(
        name="test_tool",
        dailyPrice=10.0,
        totalPrice=100.0,
        images=["image1_base64.png", "image2_base64.png"],
        features={"feature1": "value1", "feature2": "value2"},
        category="test_category",
        type="test_type",
        description="test_description"
    )

@pytest.mark.asyncio
async def test_create_tool_success(tool_repo, tool):
    tool_id = await tool_repo.create(tool)
    assert isinstance(tool_id, str)

    saved_tool = await tool_repo.tool_collection.find_one({"_id": ObjectId(tool_id)})
    assert saved_tool is not None
    assert objectId_to_str(saved_tool["_id"]) == tool_id
    assert saved_tool["name"] == tool.name
    assert saved_tool["dailyPrice"] == tool.dailyPrice
    assert saved_tool["totalPrice"] == tool.totalPrice
    assert saved_tool["images"] == tool.images
    assert saved_tool["features"] == tool.features
    assert saved_tool["rating"] == tool.rating
    assert saved_tool["ordersNumber"] == tool.ordersNumber
    assert saved_tool["category"] == tool.category
    assert saved_tool["type"] == tool.type
    assert saved_tool["description"] == tool.description

@pytest.mark.asyncio
async def test_create_tool_database_error(tool_repo, tool, monkeypatch):
    async def mock_insert_one(*args, **kwargs):
        raise PyMongoError("Mocked insertion error")

    monkeypatch.setattr(tool_repo.tool_collection, 'insert_one', mock_insert_one)

    with pytest.raises(DatabaseError):
        await tool_repo.create(tool)

@pytest.mark.asyncio
async def test_get_paginated_summary_success(tool_repo, tool):
    tool_count = 6
    tools = []
    for i in range(tool_count):
        new_tool = Tool(
            name=f"test_tool_{i}",
            dailyPrice=10.0,
            totalPrice=100.0,
            images=[f"image1_{i}.png", f"image2_{i}.png"],
            features={f"feature1_{i}": f"value1_{i}", f"feature2_{i}": f"value2_{i}"},
            reviews=[],
            rating=4.5,
            ordersNumber=10,
            category=f"test_category_{i}",
            type=f"test_type_{i}",
            description=f"test_description_{i}"
        )
        await tool_repo.create(new_tool)
        tools.append(new_tool)

    page = 1
    page_size = 3
    summaries = await tool_repo.get_paginated_summary(page, page_size)
    assert len(summaries) == page_size

    for i in range(0, 3):
        assert isinstance(summaries[i], ToolSummary)
        assert summaries[i].name == tools[i].name
        assert summaries[i].dailyPrice == tools[i].dailyPrice
        assert summaries[i].images == tools[i].images
        assert summaries[i].rating == tools[i].rating

    page = 2
    page_size = 3
    summaries = await tool_repo.get_paginated_summary(page, page_size)
    assert len(summaries) == page_size

    for i in range(3, 6):
        assert isinstance(summaries[i - 3], ToolSummary)
        assert summaries[i - 3].name == tools[i].name
        assert summaries[i - 3].dailyPrice == tools[i].dailyPrice
        assert summaries[i - 3].images == tools[i].images
        assert summaries[i - 3].rating == tools[i].rating

@pytest.mark.asyncio
async def test_get_paginated_summary_empty(tool_repo):
    page = 1
    page_size = 3
    summaries = await tool_repo.get_paginated_summary(page, page_size)
    assert summaries == []

@pytest.mark.asyncio
async def test_get_details_success(tool_repo, tool):
    tool_id = await tool_repo.create(tool)
    details = await tool_repo.get_details(tool_id)

    assert details is not None

    assert isinstance(details, ToolDetails)
    assert details.name == tool.name
    assert objectId_to_str(details.id) == tool_id
    assert details.name == tool.name
    assert details.dailyPrice == tool.dailyPrice
    assert details.images == tool.images
    assert details.rating == tool.rating
    assert details.features == tool.features
    assert details.category == tool.category
    assert details.type == tool.type
    assert details.description == tool.description

@pytest.mark.asyncio
async def test_get_details_not_found(tool_repo):
    non_existent_id = str(ObjectId())
    details = await tool_repo.get_details(non_existent_id)
    assert details is None

@pytest.mark.asyncio
async def test_get_details_database_error(tool_repo, monkeypatch):
    async def mock_find_one(*args, **kwargs):
        raise PyMongoError("Mocked find_one error")

    monkeypatch.setattr(tool_repo.tool_collection, 'find_one', mock_find_one)

    with pytest.raises(DatabaseError):
        await tool_repo.get_details(str(ObjectId()))

@pytest.mark.asyncio
async def test_get_total_count_success(tool_repo, tool):
    for _ in range(5):
        await tool_repo.create(tool)

    total_pages = await tool_repo.get_total_count()
    assert isinstance(total_pages, ToolPages)
    assert total_pages.pages == 5


@pytest.mark.asyncio
async def test_get_total_count_empty(tool_repo):
    total_pages = await tool_repo.get_total_count()
    assert isinstance(total_pages, ToolPages)
    assert total_pages.pages == 0

@pytest.mark.asyncio
async def test_get_total_count_database_error(tool_repo, monkeypatch):
    async def mock_count_documents(*args, **kwargs):
        raise PyMongoError("Mocked count error")

    monkeypatch.setattr(tool_repo.tool_collection, 'count_documents', mock_count_documents)

    with pytest.raises(DatabaseError):
        await tool_repo.get_total_count()

@pytest.mark.asyncio
async def test_exists_true(tool_repo, tool):
    await tool_repo.create(tool)
    exists = await tool_repo.exists(tool.name)
    assert exists is True


@pytest.mark.asyncio
async def test_exists_false(tool_repo):
    exists = await tool_repo.exists("Non-existent Tool")
    assert exists is False

@pytest.mark.asyncio
async def test_exists_database_error(tool_repo, monkeypatch):
    async def mock_count_documents(*args, **kwargs):
        raise PyMongoError("Mocked count_documents error")

    monkeypatch.setattr(tool_repo.tool_collection, 'count_documents', mock_count_documents)

    with pytest.raises(DatabaseError):
        await tool_repo.exists("Test Tool")