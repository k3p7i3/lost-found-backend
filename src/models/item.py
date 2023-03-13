from datetime import datetime
from pydantic import BaseModel, validator
from fastapi import UploadFile

from src.enums import ItemCategory, ItemReturn
from src.models.place import Place


def delete_timezone(dt: datetime) -> datetime:
    return dt.replace(tzinfo=None)


class ItemBase(BaseModel):
    name: str
    description: str
    category: ItemCategory
    return_way: ItemReturn
    author_id: int

    created_at: datetime
    updated_at: datetime

    _normilize_create_date = validator('created_at', allow_reuse=True)(delete_timezone)
    _normilize_update_date = validator('updated_at', allow_reuse=True)(delete_timezone)


class Item(ItemBase):
    item_id: int


class ItemCreate(ItemBase):
    place: Place | None


class PlacedItem(Item):
    place: Place | None
