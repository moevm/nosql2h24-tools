from typing import List
from fastapi import APIRouter, Depends, Query
from src.core.entities.category.category import CategoryName, CategoryCreated, CategoryWithTypes
from src.core.entities.tool.tool import ToolCreated, ToolCreate, ToolSummary, ToolDetails, ToolPages
from src.core.entities.type.type import TypeCreated, TypeSignature
from src.core.services.tool_service.tool_service import ToolService
from src.infrastructure.api.security.role_required import role_required
from src.infrastructure.services_instances import get_tool_service

tool_router = APIRouter()
category_router = APIRouter()
type_router = APIRouter()



@tool_router.post(
    path="/",
    status_code=201,
    response_model=ToolCreated
)
@role_required('worker')
async def create_tool(
        data: ToolCreate,
        tool_service: ToolService = Depends(get_tool_service)
):
    return await tool_service.create_tool(data)



@tool_router.get(
    path="/",
    status_code=200,
    response_model=List[ToolSummary]
)
async def get_paginated_tools(
        page: int = Query(1, ge=1),
        tool_service: ToolService = Depends(get_tool_service)
):
    return await tool_service.get_paginated_summary(page)




@tool_router.get(
    "/pages_count",
    status_code=200,
    response_model=ToolPages
)
async def get_pages_count(
        tool_service: ToolService = Depends(get_tool_service)
):
    print("HERE")
    return await tool_service.get_count_of_pages()



@tool_router.get(
    path="/{tool_id}",
    status_code=200,
    response_model=ToolDetails
)
async def get_tool_details(
        tool_id: str,
        tool_service: ToolService = Depends(get_tool_service)
):
    return await tool_service.get_details(tool_id)



@category_router.get(
    "/with_types",
    status_code=200,
    response_model=List[CategoryWithTypes]
)
async def get_categories_with_types(
        tool_service: ToolService = Depends(get_tool_service)
):
    return await tool_service.get_categories_with_types()



@category_router.post(
    path="/",
    status_code=201,
    response_model=CategoryCreated
)
@role_required('worker')
async def create_category(
        data: CategoryName,
        tool_service: ToolService = Depends(get_tool_service)
):
    return await tool_service.create_category(data)



@type_router.post(
    path="/",
    status_code=201,
    response_model=TypeCreated
)
@role_required('worker')
async def create_type(
        data: TypeSignature,
        tool_service: ToolService = Depends(get_tool_service)
):
    return await tool_service.create_type(data)