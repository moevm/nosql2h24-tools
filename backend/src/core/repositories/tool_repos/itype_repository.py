from abc import ABC, abstractmethod
from typing import Optional, List, Dict
from bson import ObjectId
from src.core.entities.type.type import Type, TypeSignature

class ITypeRepository(ABC):
    @abstractmethod
    async def create(self, type: Type) -> str:
        pass

    @abstractmethod
    async def get_id_by_signature(self, type_sign: TypeSignature) -> Optional[str]:
        pass

    @abstractmethod
    async def delete_by_name(self, type_sign: TypeSignature) -> int:
        pass

    @abstractmethod
    async def add_to_associated_tools(self, type_sign: TypeSignature, tool_id: str) -> int:
        pass

    @abstractmethod
    async def delete_from_associated_tools(self, type_sign: TypeSignature, tool_id: str) -> int:
        pass

    @abstractmethod
    async def exists(self, type_sign: TypeSignature) -> bool:
        pass

    @abstractmethod
    async def is_associated_tools_empty(self, type_sign: TypeSignature) -> bool:
        pass

    @abstractmethod
    async def get_types_by_ids(self, type_ids: List[ObjectId]) -> List[Dict]:
        pass