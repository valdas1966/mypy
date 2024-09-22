from typing import Generic, TypeVar, Callable
from f_abstract.mixins.nameable import Nameable
from f_abstract.mixins.iterable import Iterable
from f_utils import u_list

Item = TypeVar('Item')   # Type of Items in the Collection


class Collection1D(Generic[Item], Iterable[Item], Nameable):
    """
    ============================================================================
     Abstract-Class represents list Collection of Items.
    ============================================================================
    """

    def __init__(self,
                 items: list[Item] = None,
                 name: str = None) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        Nameable.__init__(self, name=name)
        self._items = items or list[Item]()

    def filter(self, predicate: Callable[[Item], True]) -> list[Item]:
        """
        ========================================================================
         Return List of Items that met the Predicate.
        ========================================================================
        """
        return u_list.to_filter(li=self.to_list(), predicate=predicate)

    def sample(self,
               pct: int = None,
               size: int = None,
               predicate: Callable[[Item], True] = None) -> list[Item]:
        """
        ========================================================================
         Return Sample List of Items by Pct/Size and Predicate.
        ========================================================================
        """
        return u_list.to_sample(li=self.to_list(),
                                pct=pct,
                                size=size,
                                predicate=predicate)

    def to_list(self) -> list[Item]:
        """
        ========================================================================
         Return list representation of the Object.
        ========================================================================
        """
        if isinstance(self._items, list):
            return self._items
        return list(self._items)

    def __str__(self) -> str:
        """
        ========================================================================
         Return STR-REPR of the Collection.
         Ex: Name([...])
        ========================================================================
        """
        if self._items is None:
            return f'{self.name}(None)'
        return f'{self.name}({Iterable.__str__(self)})'
