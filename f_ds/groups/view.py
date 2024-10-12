from __future__ import annotations
from f_ds.groups.group import Group, Item
from f_abstract.mixins.nameable import Nameable
from f_abstract.mixins.sizable import Sizable
from f_utils.dtypes.u_seq import USeq
from collections.abc import Iterable
from typing import Generic, Callable, Iterator


class View(Generic[Item], Nameable, Sizable, Iterable):
    """
    ============================================================================
     Dynamic and Filtered view of a Group based on a Predicate.
    ============================================================================
    """

    def __init__(self,
                 group: Group[Item],
                 predicate: Callable[[Item], bool],
                 name: str = None) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        Nameable.__init__(self, name=name)
        self._group = group
        self._predicate = predicate

    def pct(self) -> int:
        """
        ========================================================================
         Return the Percentage of Items that meet the Predicate.
        ========================================================================
        """
        total = len(self._group)
        if not total:
            return 0
        return round((len(self) / total) * 100)

    def filter(self,
               predicate: Callable[[Item], bool],
               name: str = None) -> View[Item]:
        """
        ========================================================================
         Return a new View with an additional Predicate applied.
        ========================================================================
        """
        p_comb = lambda item: self._predicate(item) and predicate(item)
        return View(group=self._group, predicate=p_comb, name=name)

    def sample(self,
               size: int = None,
               pct: int = None,
               name: str = None) -> Group[Item]:
        """
        ========================================================================
         Return a random Sample-Group by received Size/Percentage.
        ========================================================================
        """
        data = USeq.items.sample(seq=list(self), pct=pct, size=size)
        return Group(name=name, data=data)

    def __iter__(self) -> Iterator[Item]:
        """
        ========================================================================
         Allow iteration over Items that meet the Predicate.
        ========================================================================
        """
        return (item for item in self._group if self._predicate(item))

    def __len__(self) -> int:
        """
        ========================================================================
         Return the Count of Items that meet the Predicate.
        ========================================================================
        """
        return sum(1 for _ in self)

    def __str__(self) -> str:
        """
        ========================================================================
         Return Object's STR-REPR.
        ========================================================================
        """
        return f'{Nameable.__str__(self)}{list(self)}'
