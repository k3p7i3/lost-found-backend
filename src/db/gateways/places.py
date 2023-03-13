from src.db import database
from src.db.tables import places_table
from src.models.place import Location, Place


class PlacesGateway:
    table = places_table
    prim_key = 'place_id'
    model = Place

    async def get_place_by_id(self, place_id: int) -> Place | None:
        query = self.table.select().where(self.table.c.place_id == place_id)
        data = await database.fetch_one(query)

        if not data:
            return

        location = Location(latitude=data.latitude, longitude=data.longitude)
        place = Place(address=data.address, coordinates=location)
        return place

    async def insert(self, **fields) -> int:
        query = self.table.insert().values(**fields)
        return await database.execute(query)