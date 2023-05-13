from pydantic import BaseModel, validator
from src.logic.utils import hash_password, check_password_content


class User(BaseModel):
    user_id: int
    name: str
    phone_number: str
    password: str       # hash of password
    avatar_path: str | None = None


class UserOut(BaseModel):
    user_id: int
    name: str
    phone_number: str
    avatar_path: str | None = None


class UserAuth(BaseModel):
    name: str = ""
    phone_number: str
    password: str

    @validator('password')
    def check_and_hash_password(cls, v) -> str:
        if not check_password_content(v):
            raise ValueError('password too short or contains or invalid symbols')
        return hash_password(v)