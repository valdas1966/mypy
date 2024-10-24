from __future__ import annotations
from collections import UserList
from f_abstract.mixins.nameable import Nameable
from f_utils.dtypes.u_seq import USeq
from typing import TypeVar, Callable

Item = TypeVar('Item')


class Group(Nameable, UserList[Item]):
    """
    ============================================================================
     Mixin-Class for objects with lists.
    ============================================================================
    """

    def __init__(self,
                 name: str = None,
                 data: list[Item] = None) -> None:
        """
        ========================================================================
         Initialize the Listable object with the given items.
        ========================================================================
        """
        Nameable.__init__(self, name=name)
        UserList.__init__(self, data or list())

    def filter(self,
               predicate: Callable[[Item], bool],
               name: str = None) -> Group[Item]:
        """
        ========================================================================
         Return List of Items that met the Predicate.
        ========================================================================
        """
        data = USeq.items.filter(seq=self.data, predicate=predicate)
        return self.__class__(name=name, data=data)

    def sample(self,
               pct: int = None,
               size: int = None,
               name: str = None) -> Group[Item]:
        """
        ========================================================================
         Return Sample List of Items by Pct/Size and Predicate.
        ========================================================================
        """
        data = USeq.items.sample(seq=self.data, pct=pct, size=size)
        return self.__class__(name=name, data=data)

    def sample_sorted(self,
                      size: int = None,
                      pct: int = None,
                      name: str = None) -> Group[Item]:
        """
        ========================================================================
         Return Sample List of Items by Pct/Size and Predicate in Ascending Order.
         If items are not Comparable, sort by their index in the Group.
        ========================================================================
        """
        # Get a random sample
        items = USeq.items.sample(seq=self.data, size=size, pct=pct)
        items_sorted = sorted(items,
                              key=lambda item: self.data.index(item))
        return self.__class__(name=name, data=items_sorted)

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

    def key_comparison(self) -> list:
        """
        ========================================================================
         Compare by the Name of the Group.
        ========================================================================
        """
        return Nameable.key_comparison(self)

    def __iadd__(self, other: list[Item]) -> Group[Item]:
        """
        ========================================================================
         Add List of Items to the current Data.
        ========================================================================
        """
        self.data += other
        return self

    def __str__(self) -> str:
        """
        ========================================================================
         Return Object's STR-REPR.
        ========================================================================
        """
        return f'{Nameable.__str__(self)}{UserList.__str__(self)}'

    def __eq__(self, other: Group) -> bool:
        return str(self) == str(other)
