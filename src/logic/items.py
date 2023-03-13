from src.db.gateways.general import GeneralGateway
from src.models.item import Item, PlacedItem, ItemCreate, ItemBase
from src.models.mapregion import MapRegion
from src.exceptions import UserNotExistsException


class ItemLogicGateway:
    def __init__(self):
        self.gt = GeneralGateway()

    async def _create_base_item_with_place_id(self, item: ItemBase, place_id: int | None) -> int:
        if not await self.gt.users.get_user_by_id(item.author_id):
            raise UserNotExistsException(user_id=item.author_id)

        print(item.dict())
        item_id = await self.gt.items.insert(
            place_id=place_id,
            **item.dict(),
        )
        return item_id

    async def create_placed_item(self, item: ItemCreate) -> int:
        place_data = {
            'address': item.place.address,
            'latitude': item.place.coordinates.latitude,
            'longitude': item.place.coordinates.longitude,
        }
        place_id = await self.gt.places.insert(**place_data)

        item_id = await self._create_base_item_with_place_id(item=ItemBase(**item.dict()), place_id=place_id)
        return item_id

    async def get_base_item_by_id(self, item_id: int) -> Item | None:
        return await self.gt.items.get_base_item_by_id(item_id)

    async def get_placed_item_by_id(self, item_id: int) -> PlacedItem | None:
        item_data = await self.gt.items.get_item_data_by_id(item_id)
        print('Item_data:', item_data)
        if not item_data:
            return

        place = await self.gt.places.get_place_by_id(place_id=item_data['place_id'])
        return PlacedItem(place=place, **item_data)

    async def get_items_by_author(self, author_id: int) -> list[Item]:
        if await self.gt.users.check_user_exists_by_id(user_id=author_id):
            return await self.gt.items.get_base_items_by_author(author_id=author_id)

        raise UserNotExistsException(user_id=author_id)

    async def get_placed_items_on_map(self, map_region: MapRegion) -> list[PlacedItem]:
        return await self.gt.items.get_items_on_map(map_region=map_region)
