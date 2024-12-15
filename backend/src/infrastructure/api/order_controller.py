from typing import List

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer

from src.core.entities.order.order import OrderCreate, OrderCreated, Order, OrderSummary, OrderForWorker
from src.core.services.order_service import order_service
from src.core.services.order_service.order_service import OrderService
from src.infrastructure.api.security.role_required import role_required
from src.infrastructure.services_instances import get_order_service


order_router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

@order_router.post(
    path = "/{user_id}",
    status_code=201,
    response_model=OrderCreated)
@role_required('self')
async def create_order(
    user_id: str,
    data: OrderCreate,
    order_service: OrderService = Depends(get_order_service),
    token: str = Depends(oauth2_scheme)
) :
    return await order_service.create_order(data)

@order_router.get(
    path='/client/{user_id}',
    status_code=200,
    response_model=List[OrderSummary]
)
@role_required('self')
async def get_orders(
        user_id: str,
        order_service: OrderService = Depends(get_order_service),
        token: str = Depends(oauth2_scheme)
):
    return await order_service.get_all_client_orders(user_id)

@order_router.get(
    path='/worker/{user_id}',
    status_code=200,
    response_model=List[OrderForWorker]
)
@role_required('self')
async def get_orders(
        user_id: str,
        order_service: OrderService = Depends(get_order_service),
        token: str = Depends(oauth2_scheme)
):
    return await order_service.get_all_worker_orders(user_id)

@order_router.get(
    path='/{order_id}',
    status_code=200,
    response_model=Order
)
async def get_order(
        order_id: str,
        order_service: OrderService = Depends(get_order_service),
        token: str = Depends(oauth2_scheme)
):
    return await order_service.get_order_by_id(order_id)