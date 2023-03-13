from enum import Enum


class ItemCategory(str, Enum):
    phones = 'phones'
    keys = 'keys'
    documents = 'documents'
    wallets = 'wallets'
    accessories = 'accessories'
    others = 'others'


class ItemReturn(str, Enum):
    contact = 'contact'
    left = 'left'
    other = 'other'
