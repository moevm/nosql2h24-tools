from abc import ABC, abstractmethod
from src.core.entities.category.category import Category
from typing import List, Dict

class ICategoryRepository(ABC):
    @abstractmethod
    async def create(self, category: Category) -> str:
        pass

    @abstractmethod
    async def delete_by_name(self, category_name: str) -> int:
        pass

    @abstractmethod
    async def add_to_associated_types(self, category_name: str, type_id: str) -> int:
        pass

    @abstractmethod
    async def delete_from_associated_types(self, category_name: str, type_id: str) -> int:
        pass

    @abstractmethod
    async def exists(self, category_name: str) -> bool:
        pass

    @abstractmethod
    async def is_associated_types_empty(self, category_name: str) -> bool:
        pass

    @abstractmethod
    async def get_all_categories(self) -> List[Dict]:
        pass
