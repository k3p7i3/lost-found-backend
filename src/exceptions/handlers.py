from fastapi import Request, FastAPI
from fastapi.responses import JSONResponse

from src.exceptions import (
    AuthException,
    FileNotExistException,
    UserNotExistsException,
    ItemNotExistsException,
)


def add_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(AuthException)
    async def auth_exception_handler(request: Request, exc: AuthException):
        return JSONResponse(
            status_code=404,
            content={
                'type': 'authentication error',
                'details': 'wrong phone number or password',
            }
        )

    @app.exception_handler(UserNotExistsException)
    async def user_not_exists_exception_handler(request: Request, exc: UserNotExistsException):
        return JSONResponse(
            status_code=404,
            content={
                'type': 'object not exists',
                'details': 'Used with id: {id} does not exist'.format(id=exc.user_id),
            }
        )

    @app.exception_handler(ItemNotExistsException)
    async def user_not_exists_exception_handler(request: Request, exc: ItemNotExistsException):
        return JSONResponse(
            status_code=404,
            content={
                'type': 'object not exists',
                'details': 'Item with id: {id} does not exist'.format(id=exc.item_id),
            }
        )

    @app.exception_handler(FileNotExistException)
    async def file_not_exist_exception_handler(request: Request, exc: FileNotExistException):
        return JSONResponse(
            status_code=404,
            content={
                'type': 'object not exists',
                'details': 'File with path: {path} does not exist'.format(path=exc.path),
            }
        )
