from abc import ABC, abstractmethod

from src.core.entities.order.order import Order


class IOrderRepository(ABC):
    @abstractmethod
    async def create(self, order: Order) -> str:
        pass