from collections import UserList
from typing import Generic, TypeVar

Item = TypeVar('Item')


class Listable(UserList, Generic[Item]):
    """
    ============================================================================
     Mixin-Class for objects with lists.
    ============================================================================
    """

    def __init__(self, data: list[Item] = None) -> None:
        """
        ========================================================================
         Initialize the Listable object with the given items.
        ========================================================================
        """
        super().__init__(data if data is not None else list())

    def move(self, item: Item, index: int) -> None:
        """
        ========================================================================
         Move the Item to the given Index (move others forward).
        ========================================================================
        """
        self.remove(item)
        self.insert(index, item)

    def display(self) -> None:
        """
        ========================================================================
         Print the List values in rows.
        ========================================================================
        """
        for item in self.data:
            print(item)