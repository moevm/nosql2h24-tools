from abc import ABC, abstractmethod

from src.core.entities.db_model.db_model import DBModel, DBModelCreate


class IImExRepository(ABC):
    @abstractmethod
    async def export_data(self) -> DBModel:
        pass

    @abstractmethod
    async def import_data(self, data: DBModelCreate) -> None:
        pass