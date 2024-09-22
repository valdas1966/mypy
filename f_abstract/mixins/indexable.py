from f_abstract.mixins.iterable import Iterable
from typing import TypeVar

Item = TypeVar('Item')


class Indexable(Iterable[Item]):
    """
    ============================================================================
     Mixin-Class for Objects with Index.
    ============================================================================
    """

    def __init__(self, items: list[Item] = None) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        self._items = items if items is not None else list[Item]()

    def to_list(self) -> list[Item]:
        """
        ========================================================================
         Return List of all Items.
        ========================================================================
        """
        return self._items

    def insert_at(self, item: Item, index: int) -> None:
        """
        ========================================================================
         Insert an Item into a given Index (shift other items forward).
        ========================================================================
        """
        self._items.insert(index, item)

    def index_of(self, item: Item) -> int:
        """
        ========================================================================
         Return an Index of a given Item.
        ========================================================================
        """
        return self._items.index(item)

    def remove(self, item: Item) -> None:
        pass

    def move_to(self, item: Item, index: int) -> None:
        pass

    def __contains__(self, item: Item) -> bool:
        """
        ========================================================================
         Return True if the given Item is in the Object.
        ========================================================================
        """
        return item in self.to_list()

    def __getitem__(self, index: int | slice) -> int | list[Item]:
        """
        ========================================================================
         Return the Item(s) at the given index or slice.
        ========================================================================
        """
        return self.to_list()[index]
