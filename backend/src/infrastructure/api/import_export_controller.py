from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer
from fastapi.responses import FileResponse

from src.core.entities.db_model.db_model import DBModel, DBModelCreate
from src.core.services.im_ex_service.im_ex_service import ImExService
from src.infrastructure.api.client_controller import oauth2_scheme
from src.infrastructure.api.security.role_required import is_worker
from src.infrastructure.services_instances import get_im_ex_service

im_ex_router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

@im_ex_router.get(path="/export_file", status_code=201)
async def export(
        im_ex_service: ImExService = Depends(get_im_ex_service),
        token: str = Depends(oauth2_scheme),
):
    is_worker(token)
    file_path = await im_ex_service.export_file()
    return FileResponse(
        path=file_path,
        filename="data.json",
        media_type='application/octet-stream'
    )

@im_ex_router.get(path="/export", status_code=201, response_model=DBModel)
async def export(
        im_ex_service: ImExService = Depends(get_im_ex_service),
        token: str = Depends(oauth2_scheme),
):
    is_worker(token)
    return await im_ex_service.export()


@im_ex_router.post(path="/import", status_code=201, response_model=None)
async def import_data(
        data: DBModelCreate,
        im_ex_service: ImExService = Depends(get_im_ex_service),
        token: str = Depends(oauth2_scheme),
):
    is_worker(token)
    return await im_ex_service.import_data(data)
