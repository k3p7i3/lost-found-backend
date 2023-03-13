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
)

places_table = Table(
    'places',
    metadata,
    Column('place_id', types.Integer, primary_key=True),
    Column('latitude', types.Float, nullable=False),
    Column('longitude', types.Float, nullable=False),
    Column('address', types.String(length=512), nullable=True),
    # Column('country', types.String(length=32), nullable=True),
)

avatar_table = Table(
    'avatars',
    metadata,
    Column('user_id', ForeignKey('users.user_id'), primary_key=True),
    Column('image', types.LargeBinary, nullable=True),
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
)

item_images_table = Table(
    'item_images',
    metadata,
    Column('image_id', types.Integer, primary_key=True),
    Column('item_id', ForeignKey('items.item_id'), nullable=False),
    Column('image', types.LargeBinary, nullable=True),
    Column('is_first', types.Boolean, nullable=True),  # if the image is first and used on map
)
