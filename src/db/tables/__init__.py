from sqlalchemy import (
    MetaData,
    Table,
    Column,
    ForeignKey,
    types,
)

from src.enums import ItemCategory, ItemReturn

metadata = MetaData()

users_table = Table(
    'users',
    metadata,
    Column('user_id', types.Integer, primary_key=True),
    Column('name', types.String(length=64), nullable=False),
    Column('phone_number', types.String(length=32), nullable=False, unique=True),
    Column('password', types.String(length=256), nullable=False),
    Column('avatar_path', types.String(length=256), nullable=True),
)

places_table = Table(
    'places',
    metadata,
    Column('place_id', types.Integer, primary_key=True),
    Column('latitude', types.Float, nullable=False),
    Column('longitude', types.Float, nullable=False),
    Column('address', types.String(length=512), nullable=True),
)

items_table = Table(
    'items',
    metadata,
    Column('item_id', types.Integer, primary_key=True),
    Column('name', types.String(length=64), nullable=True),
    Column('description', types.String(length=1024), nullable=True),
    Column('category', types.Enum(ItemCategory), nullable=True),
    Column('author_id', ForeignKey('users.user_id'), nullable=False),
    Column('return_way', types.Enum(ItemReturn), nullable=True),
    Column('place_id', ForeignKey('places.place_id'), nullable=True),
    Column('created_at', types.DateTime, nullable=False),
    Column('updated_at', types.DateTime, nullable=False),
    Column('image_path', types.String(length=256), nullable=True),
)
