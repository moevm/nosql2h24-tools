from src.configs.paths import Paths
from src.configs.urls import Urls
from src.core.entities.users.base_user import UpdateUser, UpdatedUser, UpdateUserPassword, UpdatedUserPassword
from src.core.entities.users.client.client import ClientPrivateSummary
from src.core.exceptions.client_error import ResourceNotFoundError, InvalidPasswordProvided
from src.core.repositories.users_repos.client_repos.iclient_repository import IClientRepository
from typing import List
from src.core.utils.image_decoder.image_decoder import ImageDecoder
from src.core.utils.password_hasher.bcrypt_password_hasher import BcryptPasswordHasher


class ClientService:
    def __init__(self, client_repo: IClientRepository, paths_config: Paths, urls_config: Urls):
        self.client_repo = client_repo
        self.img_decoder = ImageDecoder(f"{urls_config.backend_base_url}{urls_config.api_prefix}", paths_config.client_img_storage_prefix_path)
        self.bcrypt_password_hasher = BcryptPasswordHasher()


    async def get_all_clients_summary(self) -> List[ClientPrivateSummary]:
        return await self.client_repo.get_all_clients_summary()

    async def update_client(self, client_id: str, update_data: UpdateUser) -> UpdatedUser:
        if not await self.client_repo.exists_by_id(client_id):
            raise ResourceNotFoundError("The client with provided id does not exist", details={"id": client_id})
        if update_data.image:
            image_url = self.img_decoder.decode_and_save_image(update_data.image, client_id)
            update_data.image = image_url

        return await self.client_repo.update_client(client_id, update_data)

    async def update_password(self, client_id: str, update_password: UpdateUserPassword) -> UpdatedUserPassword:
        if not await self.client_repo.exists_by_id(client_id):
            raise ResourceNotFoundError("The client with provided id does not exist", details={"id": client_id})
        if not self.bcrypt_password_hasher.verify_password(update_password.current_password, await self.client_repo.get_password_by_id(client_id)):
            raise InvalidPasswordProvided(details={"password": update_password.current_password})

        new_hashed_password = self.bcrypt_password_hasher.hash_password(password=update_password.new_password)

        return await self.client_repo.update_password(client_id, new_hashed_password)

    async def get_private_client_summary(self, client_id: str) -> ClientPrivateSummary:
        if not await self.client_repo.exists_by_id(client_id):
            raise ResourceNotFoundError("The client with provided id does not exist", details={"id": client_id})

        return await self.client_repo.get_private_summary_by_id(client_id)


