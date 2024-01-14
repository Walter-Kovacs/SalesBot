from .product import Product
from .product import ProductVariant
from .product import NamedElementsCollection
from .db import load_products


# PRODUCTS is a global collection of Product objects. These are products which are demonstrated by bot.
# Must be initialized when bot starts. Call load_products(PRODUCTS).
PRODUCTS: NamedElementsCollection = NamedElementsCollection(Product)
