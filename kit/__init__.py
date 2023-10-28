import logging
from dataclasses import dataclass
from typing import Dict

logger = logging.getLogger(f"bot.{__name__}")

# KITS is a global dictionary of Kit objects, which filled by 'load_kits' function.
# value - object of the Kit class, key - 'name' field of the object
KITS: Dict[str, "Kit"] = dict()  # Must be initialized when bot starts.


@dataclass
class Kit:
    name: str
    variants: Dict[
        str, "KitVariant"
    ]  # value - object of the KitVariant class, key - 'variant_title' field of the object.


@dataclass
class KitVariant:
    kit: Kit
    variant_title: str
    description: str
    price: int


def load_kits():
    KITS.clear()
    # temporary initialization
    # kit #1
    logger.debug("Temporary KITS initialization")
    kit = Kit(name="Kit #1", variants=dict())
    kit.variants["Variant #1 of the Kit #1"] = KitVariant(
        kit=kit,
        variant_title="Variant #1 of the Kit #1",
        description="description",
        price=100,
    )
    kit.variants["Variant #2 of the Kit #1"] = KitVariant(
        kit=kit,
        variant_title="Variant #2 of the Kit #1",
        description="description",
        price=100,
    )
    KITS[kit.name] = kit
    # kit #2
    kit = Kit(name="Foo", variants=dict())
    kit.variants["Variant #1 of the Foo"] = KitVariant(
        kit=kit,
        variant_title="Variant #1 of the Foo",
        description="description",
        price=100,
    )
    KITS[kit.name] = kit
