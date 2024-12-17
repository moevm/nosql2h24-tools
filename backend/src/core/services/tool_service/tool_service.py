from src.configs.paths import Paths
from src.configs.urls import Urls
from src.core.entities.category.category import Category, CategoryName, CategoryCreated, CategoryWithTypes
from src.core.entities.tool.tool import ToolCreated, ToolCreate, Tool, ToolSummary, ToolDetails, ToolPages, \
    PaginatedToolsResponse
from src.core.entities.type.type import TypeSignature, Type, TypeCreated, TypeName
from src.core.exceptions.client_error import ResourceNotFoundError, ResourceAlreadyExistsError
from src.core.repositories.tool_repos.icategory_repository import ICategoryRepository
from src.core.repositories.tool_repos.itool_repository import IToolRepository
from src.core.repositories.tool_repos.itype_repository import ITypeRepository
from src.core.utils.image_decoder.image_decoder import ImageDecoder
from typing import List, Optional

class ToolService:
    def __init__(self, tool_repo: IToolRepository, category_repo: ICategoryRepository, type_repo: ITypeRepository, paths_config: Paths, urls_config: Urls):
        self.tool_repo = tool_repo
        self.category_repo = category_repo
        self.type_repo = type_repo
        self.img_decoder = ImageDecoder(f"{urls_config.backend_base_url}{urls_config.api_prefix}", paths_config.tool_img_storage_prefix_path)

    async def create_tool(self, tool: ToolCreate) -> ToolCreated:
        if await self.tool_repo.exists(tool.name):
            raise ResourceAlreadyExistsError("A tool with this name already exists", details={"name": tool.name})
        if not await self.category_repo.exists(category_name=tool.category):
            raise ResourceNotFoundError("Provided category doesn't exist", details={"category": tool.category})
        if not await self.type_repo.exists(TypeSignature(name=tool.type, category_name=tool.category)):
            raise ResourceNotFoundError("Provided type doesn't exist", details={"type": tool.type})

        images = []

        if tool.images:
            images = self.img_decoder.decode_and_save_images(tool.images, tool.name)


        new_tool = Tool(
            name=tool.name,
            dailyPrice=tool.dailyPrice,
            totalPrice=tool.totalPrice,
            images=images,
            features=tool.features,
            category=tool.category,
            type=tool.type,
            description=tool.description
        )

        created_tool_id = await self.tool_repo.create(new_tool)
        type_sign = TypeSignature(
            name=tool.type,
            category_name=tool.category
        )

        _ = await self.type_repo.add_to_associated_tools(type_sign=type_sign, tool_id=created_tool_id)

        return ToolCreated(
            tool_id=created_tool_id
        )

    async def create_category(self, category_name: CategoryName) -> CategoryCreated:
        if await self.category_repo.exists(category_name=category_name.name):
            raise ResourceAlreadyExistsError("A category with this name already exists", details={"name": category_name.name})

        new_category = Category(name=category_name.name)
        new_category_id = await self.category_repo.create(new_category)

        return CategoryCreated(id=new_category_id)

    async def create_type(self, type_signature: TypeSignature) -> TypeCreated:
        if not await self.category_repo.exists(category_name=type_signature.category_name):
            raise ResourceNotFoundError("Provided category doesn't exist", details={"category_name": type_signature.category_name})
        if await self.type_repo.exists(type_signature):
            raise ResourceAlreadyExistsError("Provided type associated with the category name already exist", details={"name": type_signature.name, "category_name": type_signature.category_name})

        new_type = Type(
            name=type_signature.name,
            category_name=type_signature.category_name
        )
        new_type_id = await self.type_repo.create(new_type)
        _ = await self.category_repo.add_to_associated_types(category_name=type_signature.category_name, type_id=new_type_id)

        return TypeCreated(id=new_type_id)

    async def get_paginated_summary(self, page: int, page_size: int = 12) -> List[ToolSummary]:
        list_of_tool_summary = await self.tool_repo.get_paginated_summary(page, page_size)
        return list_of_tool_summary

    async def get_details(self, tool_id: str) -> ToolDetails:
        tool_details = await self.tool_repo.get_details(tool_id)

        if tool_details:
            return tool_details

        raise ResourceNotFoundError("Can't find tool by provided id", details={"id": tool_id})

    async def get_count_of_pages(self) -> ToolPages:
        tool_count = await self.tool_repo.get_total_count()
        return tool_count

    async def get_categories_with_types(self) -> List[CategoryWithTypes]:
        categories = await self.category_repo.get_all_categories()
        result = []

        for category in categories:
            type_ids = category.get("types", [])
            types = await self.type_repo.get_types_by_ids(type_ids)

            category_with_types = CategoryWithTypes(
                name=category["name"],
                types=[TypeName(name=type_doc["name"]) for type_doc in types]
            )
            result.append(category_with_types)

        return result

    async def search_tools(
            self,
            query: str,
            page: int,
            page_size: int,
            category: Optional[List[str]] = None,
            type: Optional[List[str]] = None,
            min_price: Optional[float] = None,
            max_price: Optional[float] = None
    ) -> PaginatedToolsResponse:
        total_count = await self.tool_repo.count_tools(
            query=query,
            category=category,
            type=type,
            min_price=min_price,
            max_price=max_price
        )

        tools =  await self.tool_repo.search(
            query=query,
            page=page,
            page_size=page_size,
            category=category,
            type=type,
            min_price=min_price,
            max_price=max_price
        )

        return PaginatedToolsResponse(
            tools=tools,
            totalNumber=total_count
        )