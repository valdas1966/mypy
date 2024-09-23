from typing import Generic, TypeVar

Item = TypeVar('Item')


class Listable(Generic[Item]):

    def __init__(self, items: list[Item] = None) -> None:
        self._items = items if items is not None else list()
