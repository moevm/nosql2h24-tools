import json

from src.core.entities.db_model.db_model import DBModel, DBModelCreate
from src.core.repositories.im_ex_repo.iim_ex_repo import IImExRepository


class ImExService:
    def __init__(self,
                 im_ex_repository: IImExRepository,
                 ):
        self.im_ex_repository = im_ex_repository

    async def export(self) -> DBModel:
        return await self.im_ex_repository.export_data()

    async def import_data(self, data: DBModelCreate) -> None:
        return await self.im_ex_repository.import_data(data)

    async def export_file(self) -> str:
        data = await self.im_ex_repository.export_data()
        file_path = '/tmp/data.json'
        with open(file_path, "w") as file:
            json.dump(data.model_dump(), file, default=str)
        return file_path