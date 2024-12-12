from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer

from src.core.entities.order.order import OrderCreate, OrderCreated
from src.core.services.order_service.order_service import OrderService
from src.infrastructure.services_instances import get_order_service


order_router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

@order_router.post(
    path = "/",
    status_code=201,
    response_model=OrderCreated)
async def create_order(
    data: OrderCreate,
    order_service: OrderService = Depends(get_order_service),
    token: str = Depends(oauth2_scheme)
) :
    return await order_service.create_order(data)