from f_abstract.mixins.sizable import Sizable
from f_abstract.mixins.listable import Listable
from abc import abstractmethod
from typing import Generic, TypeVar, Callable, Iterator

Item = TypeVar('Item')


class ToList(Generic[Item], Sizable):
    """
    ============================================================================
     Mixin for Classes that their content can be converted into List.
    ============================================================================
    """

    @abstractmethod
    def to_list(self) -> Listable[Item]:
        """
        ========================================================================
         Convert class content into List.
        ========================================================================
        """
        pass

    def filter(self, predicate: Callable[[Item], bool]) -> Listable[Item]:
        """
        ========================================================================
         Return List of Filtered-Items that met the Predicate.
        ========================================================================
        """
        return self.to_list().filter(predicate=predicate)

    def sample(self,
               size: int = None,
               pct: int = None) -> Listable[Item]:
        """
        ========================================================================
         Return Sample-List of Items by a given Size|Pct.
        ========================================================================
        """
        return self.to_list().sample(size=size, pct=pct)

    def __len__(self) -> int:
        """
        ========================================================================
         Return number of Items in the class content.
        ========================================================================
        """
        return len(self.to_list())

    def __iter__(self) -> Iterator[Item]:
        """
        ========================================================================
         Enable traversing over the Object's Items.
        ========================================================================
        """
        for item in self.to_list():
            yield item
