from abc import ABC, abstractmethod

from src.core.entities.db_model.db_model import DBModel


class IImExRepository(ABC):
    @abstractmethod
    async def export_data(self) -> DBModel:
        pass

    @abstractmethod
    async def import_data(self, data: DBModel) -> None:
        pass