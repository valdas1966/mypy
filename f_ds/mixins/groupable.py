from f_core.mixins.sizable import Sizable
from f_ds.groups.group import Group
from abc import abstractmethod
from typing import Generic, TypeVar, Callable, Iterator

Item = TypeVar('Item')


class Groupable(Generic[Item], Sizable):
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

    def __len__(self) -> int:
        """
        ========================================================================
         Return the number of Items in the Object.
        ========================================================================
        """
        return len(self.to_group())
    
    def __iter__(self) -> Iterator[Item]:
        """
        ========================================================================
         Return an iterator over the items in the Object.
        ========================================================================
        """
        return iter(self.to_group())
