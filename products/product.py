from dataclasses import dataclass


@dataclass
class Named:
    name: str


@dataclass
class Product(Named):
    variants: "NamedElementsCollection"


@dataclass
class ProductVariant(Named):
    product: Product
    description: str
    price: int


class CollectionException(Exception):
    pass


class NamedElementsCollection(dict):
    """
    A collection of elements of the same type, which is a subclass of Named class.
    """
    def __init__(self, elements_type: type):
        if not issubclass(elements_type, Named):
            raise CollectionException(f"Type of elements must be subclass of Named class")
        self._elements_type = elements_type
        super().__init__()

    def __iter__(self):
        return CollectionIterator(self)

    def add(self, elem: Named):
        if type(elem) != self._elements_type:
            raise CollectionException(
                f"Type of the collection elements is {self._elements_type}, type of passed element is {type(elem)}"
            )

        if not self.__contains__(elem.name):
            self[elem.name] = elem
        else:
            raise CollectionException(f"Element with name '{elem.name}' already exists")

    def get(self, elem_name: str) -> Named:
        if self.__contains__(elem_name):
            return self[elem_name]
        else:
            raise CollectionException(f"There isn't element with name '{elem_name}'")

    def names(self):
        return self.keys()


class CollectionIterator:
    """
    An iterator for NamedElementsCollection class. Collection elements are sorted by name of them.
    """
    def __init__(self, collection: NamedElementsCollection):
        self._values = [el for el in collection.values()]
        self._values.sort(key=lambda x: x.name)
        self._pointer = 0

    def __next__(self):
        if self._pointer < len(self._values):
            value = self._values[self._pointer]
            self._pointer += 1
            return value
        raise StopIteration
