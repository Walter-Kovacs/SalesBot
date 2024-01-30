from typing import (
    Dict,
    List,
)

from products import (
    ProductVariant,
)

_db: Dict[int, List[ProductVariant]] = dict()  # key: telegram user id


# Create
def create_user_list_of_variants(user_id: int):
    _db[user_id] = list()


# Read
def get_user_list_of_variants(user_id: int) -> List[ProductVariant]:
    return _db[user_id]


# Update
def add_product_variant(user_id: int, product_variant: ProductVariant):
    _db[user_id].append(product_variant)


def remove_product_variant(user_id: int, product_variant: ProductVariant):
    _db[user_id].remove(product_variant)


# Delete
def delete_user_list_of_variants(user_id: int):
    _db.pop(user_id)
