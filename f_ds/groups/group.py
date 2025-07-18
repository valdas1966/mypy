from __future__ import annotations
from collections import UserList
from f_core.mixins.has.name import HasName
from f_utils.dtypes.u_seq import USeq
from typing import TypeVar, Callable, Sequence
from math import ceil

Item = TypeVar('Item')


class Group(HasName, UserList[Item]):
    """
    ============================================================================
     Group Data-Structure (A named list with utility functions).
    ============================================================================
    """

    def __init__(self,
                 data: Sequence[Item] = None,
                 name: str = 'Group'
                 ) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        self._data = list(data) if data else list()
        HasName.__init__(self, name=name)
        UserList.__init__(self, self._data)

    def filter(self,
               predicate: Callable[[Item], bool],
               name: str = None) -> Group[Item]:
        """
        ========================================================================
         Return a filtered Group of items that meet the predicate.
        ========================================================================
        """
        data = USeq.items.filter(seq=self.data, predicate=predicate)
        return self.__class__(name=name, data=data)

    def sample(self,
               size: int = None,
               pct: int = None,
               name: str = None,
               preserve_order: bool = False) -> Group[Item]:
        """
        ========================================================================
         Return a sampled Group of items by size or percentage.
        ========================================================================
        """
        data = USeq.items.sample(seq=self.data, size=size, pct=pct)
        if preserve_order:
            data = sorted(data, key=lambda item: self.data.index(item))
        return self.__class__(name=name, data=data)

    def move(self,
             item: Item,
             index: int) -> None:
        """
        ========================================================================
         Move the item to the given index (move others forward).
        ========================================================================
        """
        self.remove(item)
        self.insert(index, item)

    def distribute(self, n: int) -> list[Group[Item]]:
        """
        ========================================================================
         Distribute the items into n groups.
        ========================================================================
        """
        size: int = ceil(len(self.data) / n)
        groups: list[Group[Item]] = list()
        for i in range(n):
            # Name of the group
            name = f'{self.name}[{i+1}]' if self.name else self.name
            # First index of the group
            first = i * size
            # Last index of the group
            last = first + size
            # Data of the group
            data = self.data[first:last]
            # Create the group
            group = Group(name=name, data=data)
            # Append the group to the list
            groups.append(group)
        return groups

    def display(self) -> None:
        """
        ========================================================================
         Print the list values in rows.
        ========================================================================
        """
        for item in self.data:
            print(item)

    def key_comparison(self) -> list:
        """
        ========================================================================
         Compare first by the name of the Group, and second by its Data.
        ========================================================================
        """
        return [HasName.key_comparison(self), self.data]

    def __iadd__(self, other: list[Item]) -> Group[Item]:
        """
        ========================================================================
         Add a list of items to the current data.
        ========================================================================
        """
        self.data.extend(other)
        return self

    def __str__(self) -> str:
        """
        ========================================================================
         Return the string representation of the Group.
        ========================================================================
        """
        return f'{HasName.__str__(self)}{self.data}'

    @classmethod
    def union(cls,
              name: str,
              groups: Sequence[Group[Item]]) -> Group[Item]:
        """
        ========================================================================
         Generate a Group by union of a sequence of Groups.
        ========================================================================
        """
        group = Group(name=name)
        for g in groups:
            group += g.data
        return group
    
    @classmethod
    def to_groups(cls,
                  data: Sequence[Item],
                  n: int,
                  name: str = None) -> list[Group[Item]]:
        """
        ========================================================================
         Convert a sequence of items into a list of groups.
        ========================================================================
        """
        group = Group(name=name, data=data)
        return group.distribute(n=n)
