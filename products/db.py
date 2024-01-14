import logging

from .product import (
    NamedElementsCollection,
    Product,
    ProductVariant,
)

logger = logging.getLogger(f"bot.{__name__}")


def load_products(products: NamedElementsCollection):
    """
    Fills passed Collection object with Product objects from file.
    :return: Collection of Product objects
    """
    products.clear()
    # temporary initialization (not from file)
    # product #1
    logger.debug("Temporary products initialization")
    product = Product(name="Product #1", variants=NamedElementsCollection(ProductVariant))
    product.variants.add(
        ProductVariant(
            product=product,
            name="Variant #1 of the Product #1",
            description="description",
            price=101,
        )
    )
    product.variants.add(
        ProductVariant(
            product=product,
            name="Variant #2 of the Product #1",
            description="description",
            price=102,
        )
    )
    products.add(product)
    # product #2
    product = Product(name="Foo", variants=NamedElementsCollection(ProductVariant))
    product.variants.add(
        ProductVariant(
            product=product,
            name="Variant #1 of the Foo",
            description="description",
            price=103,
        )
    )
    products[product.name] = product
