from pydantic import BaseModel


class Location(BaseModel):
    latitude: float
    longitude: float


class Place(BaseModel):
    address: str
    coordinates: Location
    # country: str
    # country_code: str
    # mapRegion: MapRegion
