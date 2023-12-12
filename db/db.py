from typing import (
    Dict,
    List,
)

from kit import KitVariant

_db: Dict[int, List[KitVariant]] = dict()  # key: telegram user id


# Create
def create_user_list_of_variants(user_id: int):
    _db[user_id] = list()


# Read
def get_user_list_of_variants(user_id: int) -> List[KitVariant]:
    return _db[user_id]


# Update
def add_kit_variant(user_id: int, kit_variant: KitVariant):
    _db[user_id].append(kit_variant)


def remove_kit_variant(user_id: int, kit_variant: KitVariant):
    _db[user_id].remove(kit_variant)


# Delete
def delete_user_list_of_variants(user_id: int):
    _db.pop(user_id)
