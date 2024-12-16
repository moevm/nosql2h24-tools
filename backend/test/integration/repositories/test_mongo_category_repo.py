from unittest.mock import AsyncMock
import pytest, pytest_asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
from src.configs.config import config
from src.core.entities.category.category import Category
from src.core.entities.object_id_str import ObjectIdStr
from src.core.exceptions.server_error import DatabaseError
from src.infrastructure.repo_implementations.helpers.id_mapper import str_to_objectId, objectId_to_str
from src.infrastructure.repo_implementations.tool_repos.mongo_category_repository import MongoCategoryRepository
from pymongo.errors import PyMongoError

@pytest_asyncio.fixture(scope='function')
async def db():
    client = AsyncIOMotorClient(str(config.mongo.mongo_dsn))
    database = client[config.mongo.mongo_db]

    await database.drop_collection(config.collections.category_collection)

    yield database

    await database.drop_collection(config.collections.category_collection)
    client.close()

@pytest_asyncio.fixture(scope='function')
async def category_repo(db):
    return MongoCategoryRepository(db, config.collections.category_collection)

@pytest.fixture
def category():
    type_ids = [ObjectIdStr(), ObjectIdStr()]
    return Category(
        name="test-category",
        types=type_ids
    )


@pytest.mark.asyncio
async def test_create_category_success(category_repo, category):
    category_id = await category_repo.create(category)
    assert isinstance(category_id, str)

    saved_category = await category_repo.category_collection.find_one({"_id": str_to_objectId(category_id)})

    assert saved_category is not None
    assert objectId_to_str(saved_category["_id"]) == category_id
    assert saved_category["name"] == category.name
    assert saved_category["types"] == [ObjectId(t_id) for t_id in category.types]

@pytest.mark.asyncio
async def test_create_category_database_error(category_repo, category, monkeypatch):
    async def mock_insert_one(*args, **kwargs):
        raise PyMongoError("Mocked insertion error")

    monkeypatch.setattr(category_repo.category_collection, 'insert_one', mock_insert_one)

    with pytest.raises(DatabaseError):
        await category_repo.create(category)


@pytest.mark.asyncio
async def test_delete_by_name_success(category_repo, category):
    await category_repo.create(category)
    deleted_count = await category_repo.delete_by_name(category.name)
    assert deleted_count == 1

    exists = await category_repo.category_collection.count_documents({"name": category.name})
    assert not exists

@pytest.mark.asyncio
async def test_delete_by_name_not_found(category_repo):
    deleted_count = await category_repo.delete_by_name("non_existent_category")
    assert deleted_count == 0

@pytest.mark.asyncio
async def test_delete_by_name_database_error(category_repo, monkeypatch):
    async def mock_delete_one(*args, **kwargs):
        raise PyMongoError("Mocked deletion error")

    monkeypatch.setattr(category_repo.category_collection, 'delete_one', mock_delete_one)

    with pytest.raises(DatabaseError):
        await category_repo.delete_by_name("test_category")

@pytest.mark.asyncio
async def test_add_to_associated_types_success(category_repo, category):
    await category_repo.create(category)
    initial_category = await category_repo.category_collection.find_one({"name": category.name})
    initial_types_count = len(initial_category["types"])

    new_type_id = str(ObjectId())
    modified_count = await category_repo.add_to_associated_types(category.name, new_type_id)
    assert modified_count == 1

    updated_category = await category_repo.category_collection.find_one({"name": category.name})
    assert updated_category is not None
    assert ObjectId(new_type_id) in updated_category["types"]
    assert len(updated_category["types"]) == initial_types_count + 1

@pytest.mark.asyncio
async def test_add_to_associated_types_category_not_found(category_repo):
    type_id = str(ObjectId())
    modified_count = await category_repo.add_to_associated_types("non_existent_category", type_id)
    assert modified_count == 0

@pytest.mark.asyncio
async def test_add_to_associated_types_database_error(category_repo, monkeypatch):
    async def mock_update_one(*args, **kwargs):
        raise PyMongoError("Mocked update error")

    monkeypatch.setattr(category_repo.category_collection, 'update_one', mock_update_one)

    with pytest.raises(DatabaseError):
        await category_repo.add_to_associated_types("test_category", str(ObjectId()))

@pytest.mark.asyncio
async def test_delete_from_associated_types_success(category_repo, category):
    await category_repo.create(category)
    type_id_to_remove = category.types[0]
    modified_count = await category_repo.delete_from_associated_types(category.name, type_id_to_remove)
    assert modified_count == 1

    updated_category = await category_repo.category_collection.find_one({"name": category.name})
    assert updated_category is not None
    assert ObjectId(type_id_to_remove) not in updated_category["types"]
    assert len(updated_category["types"]) == len(category.types) - 1

@pytest.mark.asyncio
async def test_delete_from_associated_types_category_not_found(category_repo):
    type_id = str(ObjectId())
    modified_count = await category_repo.delete_from_associated_types("non_existent_category", type_id)
    assert modified_count == 0

@pytest.mark.asyncio
async def test_delete_from_associated_types_database_error(category_repo, monkeypatch):
    async def mock_update_one(*args, **kwargs):
        raise PyMongoError("Mocked update error")

    monkeypatch.setattr(category_repo.category_collection, 'update_one', mock_update_one)

    with pytest.raises(DatabaseError):
        await category_repo.delete_from_associated_types("test_category", str(ObjectId()))

@pytest.mark.asyncio
async def test_exists_true(category_repo, category):
    await category_repo.create(category)
    exists = await category_repo.exists(category.name)
    assert exists is True

@pytest.mark.asyncio
async def test_exists_false(category_repo):
    exists = await category_repo.exists("non_existent_category")
    assert exists is False

@pytest.mark.asyncio
async def test_exists_database_error(category_repo, monkeypatch):
    async def mock_count_documents(*args, **kwargs):
        raise PyMongoError("Mocked count error")

    monkeypatch.setattr(category_repo.category_collection, 'count_documents', mock_count_documents)

    with pytest.raises(DatabaseError):
        await category_repo.exists("test_category")


@pytest.mark.asyncio
async def test_is_associated_types_empty_false(category_repo, category):
    await category_repo.create(category)
    is_empty = await category_repo.is_associated_types_empty(category.name)
    assert is_empty is False

@pytest.mark.asyncio
async def test_is_associated_types_empty_true(category_repo, category):
    category.types = []
    await category_repo.create(category)
    is_empty = await category_repo.is_associated_types_empty(category.name)
    assert is_empty is True

@pytest.mark.asyncio
async def test_is_associated_types_empty_category_not_found(category_repo):
    is_empty = await category_repo.is_associated_types_empty("non_existent_category")
    assert is_empty is True

@pytest.mark.asyncio
async def test_is_associated_types_empty_database_error(category_repo, monkeypatch):
    async def mock_find_one(*args, **kwargs):
        raise PyMongoError("Mocked find error")

    monkeypatch.setattr(category_repo.category_collection, 'find_one', mock_find_one)

    with pytest.raises(DatabaseError):
        await category_repo.is_associated_types_empty("test_category")

@pytest.mark.asyncio
async def test_get_all_categories_multiple(category_repo):
    category_count = 9

    categories = [
        Category(
            name=f"category-{i}",
            types=[ObjectIdStr(), ObjectIdStr()]
        ) for i in range(category_count)
    ]

    for category in categories:
        await category_repo.create(category)

    all_categories = await category_repo.get_all_categories()
    assert len(all_categories) == category_count

    for i in range(category_count):
        assert all_categories[i]["name"] == categories[i].name
        assert all_categories[i]["types"] == categories[i].types

@pytest.mark.asyncio
async def test_get_all_categories_empty(category_repo):
    all_categories = await category_repo.get_all_categories()
    assert all_categories == []

@pytest.mark.asyncio
async def test_get_all_categories_database_error(category_repo, monkeypatch):
    mock_cursor = AsyncMock()
    mock_cursor.to_list.side_effect = PyMongoError("Mocked to_list error")

    def mock_find(*args, **kwargs):
        return mock_cursor

    monkeypatch.setattr(category_repo.category_collection, 'find', mock_find)

    with pytest.raises(DatabaseError):
        await category_repo.get_all_categories()