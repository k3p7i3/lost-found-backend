from sqlalchemy import select, and_

from src.db import database
from src.db.tables import items_table, places_table
from src.models.item import Item, PlacedItem
from src.models.mapregion import MapRegion
from src.models.place import Location, Place


class ItemsGateway:
    table = items_table
    prim_key = 'item_id'
    model = Item

    async def get_base_item_by_condition(self, condition) -> Item | None:
        query = self.table.select().where(condition)
        data = await database.fetch_one(query)
        if data:
            return self.model(**data._mapping)

    async def get_base_item_by_id(self, item_id: int) -> Item | None:
        item = await self.get_base_item_by_condition(self.table.c.item_id == item_id)
        return item

    async def get_item_data_by_id(self, item_id: int) -> dict:
        query = self.table.select().where(self.table.c.item_id == item_id)
        data = await database.fetch_one(query)
        return dict(**data._mapping) if data else dict()

    async def get_items_by_author(self, author_id: int) -> list[Item]:
        query = self.table.select().where(self.table.c.author_id == author_id)
        rows = await database.fetch_all(query)
        items = []
        for row in rows:
            items.append(self.model(**row._mapping))
        return items

    async def insert(self, **fields) -> int:
        query = self.table.insert().values(**fields)
        return await database.execute(query)

    async def update(self, item_id: int, **fields):
        query = (
            self.table
            .update()
            .where(self.table.c[self.prim_key] == item_id)
            .values(**fields)
        )
        return await database.execute(query)

    def get_items_with_place_query(self, select_list: list):
        query = (
            select(select_list)
            .select_from(self.table.join(places_table))
            .where(self.table.c.place_id == places_table.c.place_id)
        )
        return query

    def row_to_placed_item(self, row) -> PlacedItem:
        location = Location(latitude=row.latitude, longitude=row.longitude)
        place = Place(
            address=row.address,
            country=row.country,
            coordinates=location,
        )
        item = PlacedItem(
            place=place,
            **row._mapping,
        )
        return item

    def _clause_filter_by_map_region(self, map_region: MapRegion):
        where_clause = and_(
            map_region.southLatitude <= places_table.c.latitude,
            places_table.c.latitude <= map_region.northLatitude,
            map_region.westLongitude <= places_table.c.longitude,
            places_table.c.longitude <= map_region.eastLongitude,
        )
        return where_clause

    async def get_items_on_map(self, map_region: MapRegion) -> list[PlacedItem]:
        query = self.get_items_with_place_query(select_list=[self.table, places_table])
        query = query.where(self._clause_filter_by_map_region(map_region))

        rows = await database.fetch_all(query)
        items = []
        for row in rows:
            item = self.row_to_placed_item(row)
            items.append(item)
        return items
