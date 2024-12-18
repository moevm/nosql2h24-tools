from src.core.entities.db_model.db_model import DBModel
from src.core.repositories.im_ex_repo.iim_ex_repo import IImExRepository


class ImExService:
    def __init__(self,
                 im_ex_repository: IImExRepository,
                 ):
        self.im_ex_repository = im_ex_repository

    async def export(self) -> DBModel:
        return await self.im_ex_repository.export_data()

    async def import_data(self, data: DBModel) -> None:
        return await self.im_ex_repository.import_data(data)