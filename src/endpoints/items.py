from fastapi import APIRouter, UploadFile, File
from fastapi.responses import FileResponse

from src.config import settings
from src.logic.items import ItemLogicGateway
from src.models.item import PlacedItem, ItemCreate
from src.models.mapregion import MapRegion
from src.exceptions import ItemNotExistsException, FileNotExistException

router = APIRouter()


@router.post(path='/create', status_code=201)
async def create_item(item: ItemCreate):
    pdg = ItemLogicGateway()
    new_item_id = await pdg.create_item(item)
    return {
        'status': 'success',
        'item_id': new_item_id,
    }


@router.post(path='/create/image/{item_id}', status_code=201)
async def create_item_image(item_id: int, image: UploadFile = File()):
    pdg = ItemLogicGateway()
    path = await pdg.create_item_image(item_id=item_id, image=image)
    return {
        'status': 'success',
        'path': path
    }


@router.get(path='/on_map')
async def get_items_on_map(
    east_longitude: float,
    west_longitude: float,
    north_latitude: float,
    south_latitude: float,
):
    pdg = ItemLogicGateway()
    map_region = MapRegion(
        eastLongitude=east_longitude,
        westLongitude=west_longitude,
        northLatitude=north_latitude,
        southLatitude=south_latitude,
    )
    return {
        "items": await pdg.get_placed_items_on_map(map_region=map_region)
    }


@router.get(path='/{item_id}', response_model=PlacedItem)
async def get_item(item_id: int):
    pdg = ItemLogicGateway()
    item = await pdg.get_placed_item_by_id(item_id=item_id)
    if not item:
        raise ItemNotExistsException(item_id=item_id)
    return item


@router.get(path='/images/{file_name}')
async def get_item_image(file_name: str):
    path = settings.ITEMS_STORAGE + '/' + file_name
    pdg = ItemLogicGateway()
    if pdg.gt.files.check_file_exist(path):
        return FileResponse(path)
    raise FileNotExistException

