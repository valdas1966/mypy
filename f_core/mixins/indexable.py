from collections.abc import MutableSequence
from f_core.mixins.nameable import Nameable
from typing import Generic, TypeVar

Item = TypeVar('Item')


class Indexable(Generic[Item], Nameable, MutableSequence[Item]):
    """
    ============================================================================
     Mixin-Class for Objects with Indexable Lists (without duplicate items).
    ============================================================================
    """

    def __init__(self,
                 name: str = None,
                 items: list[Item] = None) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        Nameable.__init__(self, name=name)
        self._items = items if items is not None else list()

    @property
    def items(self) -> list[Item]:
        """
        ========================================================================
         Return List of Object's Items.
        ========================================================================
        """
        return self._items

    def insert(self, index: int, item: Item) -> None:
        """
        ========================================================================
         Insert an Item into a specified Index.
        ========================================================================
        """
        self._items.insert(index, item)

    def move_to(self, item: Item, index: int) -> None:
        """
        ========================================================================
         Move an Item to a given Index.
        ========================================================================
        """
        self.remove(value=item)
        self.insert(item=item, index=index)

    def __getitem__(self, index: int | slice) -> Item | list[Item]:
        """
        ========================================================================
         Return the Item(s) at the given index or slice.
        ========================================================================
        """
        return self.items[index]

    def __len__(self) -> int:
        """
        ========================================================================
         Return the number of Object's Items.
        ========================================================================
        """
        return len(self._items)

    def __setitem__(self, index: int, value: Item) -> None:
        """
        ========================================================================
         Set a given Item into a given Index.
        ========================================================================
        """
        self._items[index] = value

    def __delitem__(self, index: int) -> None:
        """
        ========================================================================
         Delete an Item at the given Index.
        ========================================================================
        """
        del self._items[index]
