from fastapi import UploadFile

from src.models.user import User, UserAuth
from src.db.gateways.general import GeneralGateway
from src.logic.utils import check_password_match
from src.exceptions import AuthException
from src.config import settings


class UserLogicGateway:
    def __init__(self):
        self.gt = GeneralGateway()

    async def is_phone_number_unique(self, phone_number: str) -> bool:
        return not await self.gt.users.if_phone_number_exists(phone_number)

    async def registrate_user(self, user: UserAuth):
        if await self.is_phone_number_unique(user.phone_number):
            user_id = await self.gt.users.insert(**user.dict())
            return user_id
        else:
            raise AuthException()

    async def get_user(self, user_id: int):
        return await self.gt.users.get_user_by_id(user_id)

    async def auth_user(self, user: UserAuth) -> User | None:
        db_user = await self.gt.users.get_user_by_phone_number(user.phone_number)
        if db_user and check_password_match(user.password, db_user.password):
            return db_user

    async def create_user_image(self, user_id: int, image: UploadFile) -> str:
        avatar_path = settings.USERS_STORAGE + '/' + str(user_id) + '.jpeg'
        await self.gt.files.save_upload_file(avatar_path, image)
        avatar_path = avatar_path[len(settings.ITEMS_STORAGE) + 1:]
        await self.gt.users.update(user_id=user_id, avatar_path=avatar_path)
        return avatar_path
