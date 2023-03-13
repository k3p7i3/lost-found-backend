from src.db.gateways import (
    users,
    items,
    places,
)


class GeneralGateway:
    def __init__(self):
        self.users = users.UsersGateway()
        self.items = items.ItemsGateway()
        self.places = places.PlacesGateway()