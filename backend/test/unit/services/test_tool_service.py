from unittest.mock import AsyncMock, MagicMock
import pytest
from src.configs.paths import Paths
from src.configs.urls import Urls
from src.core.entities.category.category import CategoryName, CategoryCreated
from src.core.entities.tool.tool import ToolCreate, ToolCreated, Tool, ToolDetails, ToolPages
from src.core.entities.type.type import TypeSignature, TypeCreated, Type
from src.core.exceptions.client_error import ResourceAlreadyExistsError, ResourceNotFoundError
from src.core.services.tool_service.tool_service import ToolService


@pytest.fixture
def tool_repo():
    return AsyncMock()

@pytest.fixture
def category_repo():
    return AsyncMock()

@pytest.fixture
def type_repo():
    return AsyncMock()

@pytest.fixture
def paths_config():
    return Paths()

@pytest.fixture
def urls_config():
    return Urls()

@pytest.fixture
def img_decoder():
    mock_decoder = MagicMock()
    mock_decoder.decode_and_save_images.return_value = ["image1.jpg", "image2.jpg"]
    return mock_decoder

@pytest.fixture
def tool_service(tool_repo, category_repo, type_repo, paths_config, urls_config, img_decoder):
    service = ToolService(tool_repo, category_repo, type_repo, paths_config, urls_config)
    service.img_decoder = img_decoder
    return service

@pytest.fixture
def tool_create():
    return ToolCreate(
        name="test-name",
        dailyPrice=100.0,
        totalPrice=5000,
        images=["base64img1", "base64img2"],
        features={"param1": "key1", "param2": "key2"},
        category="test-category",
        type="test-type",
        description="test-description"
    )

@pytest.fixture
def tool_details():
    return ToolDetails(
        id="test-id",
        name="test-name",
        dailyPrice = 100.0,
        images=["image1.png", "image2.png"],
        rating=4.6,
        features={"param1": "key1", "param2": "key2"},
        category="test-category",
        type="test-type",
        description="test-description"
    )

@pytest.fixture
def type_signature():
    return TypeSignature(name="test-type", category_name="test-category")


@pytest.mark.asyncio
async def test_create_tool_success(tool_service, tool_repo, category_repo, type_repo, img_decoder, tool_create):
    tool_repo.exists.return_value = False
    category_repo.exists.return_value = True
    type_repo.exists.return_value = True
    tool_repo.create.return_value = "new_tool_id"
    type_repo.add_to_associated_tools.return_value = 1
    img_decoder.decode_and_save_images.return_value = ["image1.jpg", "image2.jpg"]

    result = await tool_service.create_tool(tool_create)

    assert isinstance(result, ToolCreated)
    assert result.tool_id == "new_tool_id"

    tool_repo.exists.assert_called_once_with(tool_create.name)
    category_repo.exists.assert_called_once_with(category_name=tool_create.category)
    type_repo.exists.assert_called_once_with(TypeSignature(name=tool_create.type, category_name=tool_create.category))
    img_decoder.decode_and_save_images.assert_called_once_with(tool_create.images, tool_create.name)
    tool_repo.create.assert_called_once()
    type_repo.add_to_associated_tools.assert_called_once()

@pytest.mark.asyncio
async def test_create_tool_name_already_exists(tool_service, tool_repo, category_repo, type_repo, tool_create):
    tool_repo.exists.return_value = True

    with pytest.raises(ResourceAlreadyExistsError):
        await tool_service.create_tool(tool_create)

    tool_repo.exists.assert_called_once_with(tool_create.name)
    category_repo.exists.assert_not_called()
    type_repo.exists.assert_not_called()

@pytest.mark.asyncio
async def test_create_tool_category_not_found(tool_service, tool_repo, category_repo, type_repo, tool_create):
    tool_repo.exists.return_value = False
    category_repo.exists.return_value = False

    with pytest.raises(ResourceNotFoundError):
        await tool_service.create_tool(tool_create)

    tool_repo.exists.assert_called_once_with(tool_create.name)
    category_repo.exists.assert_called_once_with(category_name=tool_create.category)
    type_repo.exists.assert_not_called()

@pytest.mark.asyncio
async def test_create_tool_type_not_found(tool_service, tool_repo, category_repo, type_repo, tool_create):
    tool_repo.exists.return_value = False
    category_repo.exists.return_value = True
    type_repo.exists.return_value = False

    with pytest.raises(ResourceNotFoundError):
        await tool_service.create_tool(tool_create)

    tool_repo.exists.assert_called_once_with(tool_create.name)
    category_repo.exists.assert_called_once_with(category_name=tool_create.category)
    type_repo.exists.assert_called_once_with(TypeSignature(name=tool_create.type, category_name=tool_create.category))

@pytest.mark.asyncio
async def test_create_category_success(tool_service, category_repo):
    category_name = CategoryName(name="test-category")
    category_repo.exists.return_value = False
    category_repo.create.return_value = "new_category_id"

    result = await tool_service.create_category(category_name)

    assert isinstance(result, CategoryCreated)
    assert result.id == "new_category_id"
    category_repo.exists.assert_called_once_with(category_name=category_name.name)
    category_repo.create.assert_called_once()

@pytest.mark.asyncio
async def test_create_category_already_exists(tool_service, category_repo):
    category_name = CategoryName(name="Tools")
    category_repo.exists.return_value = True

    with pytest.raises(ResourceAlreadyExistsError):
        await tool_service.create_category(category_name)

    category_repo.exists.assert_called_once_with(category_name=category_name.name)

@pytest.mark.asyncio
async def test_create_type_success(tool_service, category_repo, type_repo, type_signature):
    category_repo.exists.return_value = True
    type_repo.exists.return_value = False
    type_repo.create.return_value = "new_type_id"
    category_repo.add_to_associated_types.return_value = None

    result = await tool_service.create_type(type_signature)

    assert isinstance(result, TypeCreated)
    assert result.id == "new_type_id"

    category_repo.exists.assert_called_once_with(category_name=type_signature.category_name)
    type_repo.exists.assert_called_once_with(type_signature)
    type_repo.create.assert_called_once_with(Type(name=type_signature.name, category_name=type_signature.category_name))
    category_repo.add_to_associated_types.assert_called_once_with(category_name=type_signature.category_name, type_id="new_type_id")

@pytest.mark.asyncio
async def test_create_type_category_not_found(tool_service, category_repo, type_repo, type_signature):
    category_repo.exists.return_value = False

    with pytest.raises(ResourceNotFoundError):
        await tool_service.create_type(type_signature)

    category_repo.exists.assert_called_once_with(category_name=type_signature.category_name)
    type_repo.exists.assert_not_called()

@pytest.mark.asyncio
async def test_create_type_already_exists(tool_service, category_repo, type_repo, type_signature):
    category_repo.exists.return_value = True
    type_repo.exists.return_value = True

    with pytest.raises(ResourceAlreadyExistsError):
        await tool_service.create_type(type_signature)

    category_repo.exists.assert_called_once_with(category_name=type_signature.category_name)
    type_repo.exists.assert_called_once_with(type_signature)

@pytest.mark.asyncio
async def test_get_details_success(tool_service, tool_repo, tool_details):
    tool_repo.get_details.return_value = tool_details

    result = await tool_service.get_details(str(tool_details.id))

    assert isinstance(result, ToolDetails)
    assert result == tool_details

    tool_repo.get_details.assert_called_once_with(str(tool_details.id))

@pytest.mark.asyncio
async def test_get_details_not_found(tool_service, tool_repo):
    tool_repo.get_details.return_value = None

    with pytest.raises(ResourceNotFoundError):
        await tool_service.get_details("invalid_tool_id")

    tool_repo.get_details.assert_called_once_with("invalid_tool_id")

@pytest.mark.asyncio
async def test_get_count_of_pages(tool_service, tool_repo):
    tool_repo.get_total_count.return_value = ToolPages(pages=10)

    result = await tool_service.get_count_of_pages()

    assert isinstance(result, ToolPages)
    assert result.pages == 10

    tool_repo.get_total_count.assert_called_once()

@pytest.mark.asyncio
async def test_get_categories_with_types(tool_service, category_repo, type_repo):

    category_repo.get_all_categories.return_value = [
        {
            "name": "Category1",
            "types": [
                "type_id_1",
                "type_id_2"
            ]
        },
        {
            "name": "Category2",
            "types": [

            ]
        }
    ]
    type_repo.get_types_by_ids.side_effect = [
        [
            {"name": "Type1"},
            {"name": "Type2"}
        ],
        [

        ]
    ]

    result = await tool_service.get_categories_with_types()

    assert len(result) == 2
    assert result[0].name == "Category1"
    assert len(result[0].types) == 2
    assert result[0].types[0].name == "Type1"
    assert result[0].types[1].name == "Type2"
    assert result[1].name == "Category2"
    assert len(result[1].types) == 0

    category_repo.get_all_categories.assert_called_once()
    type_repo.get_types_by_ids.assert_any_call(["type_id_1", "type_id_2"])
    type_repo.get_types_by_ids.assert_any_call([])
