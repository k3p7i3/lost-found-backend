from src.db.gateways import (
    users,
    items,
    places,
    files,
)


class GeneralGateway:
    def __init__(self):
        self.users = users.UsersGateway()
        self.items = items.ItemsGateway()
        self.places = places.PlacesGateway()
        self.files = files.FileGateway()