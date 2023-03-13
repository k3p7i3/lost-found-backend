from fastapi import APIRouter

from src.endpoints import items
from src.endpoints import users

api_router = APIRouter()

api_router.include_router(users.router, prefix='/users', tags=['user'])
api_router.include_router(items.router, prefix='/items', tags=['item'])