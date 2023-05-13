class AuthException(Exception):
    def __init__(self):
        pass


class UserNotExistsException(Exception):
    def __init__(self, user_id):
        self.user_id = user_id


class ItemNotExistsException(Exception):
    def __init__(self, item_id):
        self.item_id = item_id


class FileNotExistException(Exception):
    def __init__(self, path):
        self.path = path