from pydantic import BaseModel


class MapRegion(BaseModel):
    eastLongitude: float
    westLongitude: float
    northLatitude: float
    southLatitude: float
