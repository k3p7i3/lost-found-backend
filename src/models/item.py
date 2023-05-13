from datetime import datetime
from pydantic import BaseModel, validator
from fastapi import UploadFile

from src.enums import ItemCategory, ItemReturn
from src.models.place import Place


class ItemBase(BaseModel):
    name: str
    description: str
    category: ItemCategory
    return_way: ItemReturn
    author_id: int

    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()


class Item(ItemBase):
    item_id: int
    image_path: str | None = None


class ItemCreate(ItemBase):
    place: Place | None


class PlacedItem(Item):
    place: Place | None
