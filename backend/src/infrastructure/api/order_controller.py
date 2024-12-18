from typing import List, Optional
from datetime import datetime
from fastapi import APIRouter, Depends, Query
from fastapi.security import OAuth2PasswordBearer
from pydantic import PositiveInt
from src.core.entities.order.order import OrderCreate, OrderCreated, Order, OrderSummary, OrderForWorker, \
    PaginatedOrdersResponseForWorker, PaginatedOrdersResponseForClient
from src.core.services.order_service import order_service
from src.core.services.order_service.order_service import OrderService
from src.infrastructure.api.security.role_required import is_worker, is_self
from src.infrastructure.services_instances import get_order_service


order_router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

@order_router.post(
    path = "/{user_id}",
    status_code=201,
    response_model=OrderCreated)
async def create_order(
    user_id: str,
    data: OrderCreate,
    order_service: OrderService = Depends(get_order_service),
    token: str = Depends(oauth2_scheme)
):
    is_self(token, user_id)
    return await order_service.create_order(data)


@order_router.get(
    path='/client/paginated/{user_id}',
    status_code=200,
    response_model=PaginatedOrdersResponseForClient
)
async def get_paginated_orders_for_client(
        user_id: str,
        page: PositiveInt = Query(1),
        page_size: PositiveInt = Query(12),
        tool_name: Optional[List[str]] = Query(None),
        delivery_state: Optional[str] = Query(None),
        start_date: Optional[datetime] = Query(None),
        end_date: Optional[datetime] = Query(None),
        min_price: Optional[float] = Query(None),
        max_price: Optional[float] = Query(None),
        order_service: OrderService = Depends(get_order_service),
        token: str = Depends(oauth2_scheme)
):
    is_self(token, user_id)

    return await order_service.get_paginated_orders_for_client(
        user_id=user_id,
        page=page,
        page_size=page_size,
        tool_name=tool_name,
        status=delivery_state,
        start_date=start_date,
        end_date=end_date,
        min_price=min_price,
        max_price=max_price
    )




@order_router.get(
    path='/worker/paginated',
    status_code=200,
    response_model=PaginatedOrdersResponseForWorker
)
async def get_paginated_orders_for_worker(
        page: PositiveInt = Query(1),
        page_size: PositiveInt = Query(12),
        customer_name: Optional[str] = Query(None),
        customer_surname: Optional[str] = Query(None),
        tool_name: Optional[List[str]] = Query(None),
        delivery_state: Optional[str] = Query(None),
        start_date: Optional[datetime] = Query(None),
        end_date: Optional[datetime] = Query(None),
        min_price: Optional[float] = Query(None),
        max_price: Optional[float] = Query(None),
        order_service: OrderService = Depends(get_order_service),
        token: str = Depends(oauth2_scheme)
):
    is_worker(token)
    return await order_service.get_paginated_orders_for_worker(
        page=page,
        page_size=page_size,
        customer_name=customer_name,
        customer_surname=customer_surname,
        tool_name=tool_name,
        status=delivery_state,
        start_date=start_date,
        end_date=end_date,
        min_price=min_price,
        max_price=max_price
    )



@order_router.get(
    path='/{order_id}',
    status_code=200,
    response_model=Optional[OrderSummary]
)
async def get_order(
        order_id: str,
        order_service: OrderService = Depends(get_order_service)
):
    return await order_service.get_order_by_id(order_id)