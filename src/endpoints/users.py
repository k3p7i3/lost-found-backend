from fastapi import APIRouter, UploadFile, File
from fastapi.responses import FileResponse

from src.config import settings
from src.models.user import UserOut, UserAuth
from src.logic.users import UserLogicGateway
from src.logic.items import ItemLogicGateway
from src.exceptions import AuthException, UserNotExistsException, FileNotExistException
from src.models.item import Item

router = APIRouter()


@router.post(path='/registration', status_code=201)
async def registrate_user(user: UserAuth):
    pdg = UserLogicGateway()
    new_user = await pdg.registrate_user(user)
    return {
        'status': 'success',
        'user_id': new_user,
    }


@router.post(path='/login', response_model=UserOut)
async def login_user(user: UserAuth):
    pdg = UserLogicGateway()
    user_data = await pdg.auth_user(user)
    if not user_data:
        raise AuthException()
    return user_data


@router.get(path='/{user_id}', response_model=UserOut)
async def get_user(user_id: int):
    pdg = UserLogicGateway()
    user = await pdg.get_user(user_id)
    if not user:
        raise UserNotExistsException(user_id=user_id)
    return user


@router.get(path='/images/{file_name}')
async def get_user_image(file_name: str):
    path = settings.USERS_STORAGE + '/' + file_name
    pdg = UserLogicGateway()
    if pdg.gt.files.check_file_exist(path):
        return FileResponse(path)
    raise FileNotExistException


@router.post(path='/create/image/{user_id}', status_code=201)
async def create_user_image(user_id: int, image: UploadFile = File()):
    pdg = UserLogicGateway()
    path = await pdg.create_user_image(user_id=user_id, image=image)
    return {
        'status': 'success',
        'path': path
    }


@router.get(path='/{user_id}/items', response_model=list[Item])
async def get_items_by_user(user_id: int):
    pdg = ItemLogicGateway()
    return await pdg.get_items_by_author(author_id=user_id)