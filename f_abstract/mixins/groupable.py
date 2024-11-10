from f_ds.groups.group import Group
from abc import abstractmethod
from typing import Generic, TypeVar, Callable

Item = TypeVar('Item')


class Groupable(Generic[Item]):
    """
    ============================================================================
     Mixin for classes whose content can be converted into a Group.
    ============================================================================
    """

    @abstractmethod
    def to_group(self, name: str = None) -> Group[Item]:
        """
        ========================================================================
         Convert the class content into a Group instance.
        ========================================================================
        """
        pass

    def filter(self,
               predicate: Callable[[Item], bool],
               name: str = None) -> Group[Item]:
        """
        ========================================================================
         Return a filtered Group of items that meet the given predicate.
        ========================================================================
        """
        return self.to_group().filter(name=name, predicate=predicate)

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
        return self.to_group().sample(size=size,
                                      pct=pct,
                                      name=name,
                                      preserve_order=preserve_order)
