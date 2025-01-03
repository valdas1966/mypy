from typing import TypeVar, Generic, Callable
from f_utils.dtypes.inner.list.items import Items

Item = TypeVar('Item')


class Indexes(Generic[Item]):
    """
    ============================================================================
     Utils-Class for Indexes operations on Lists.
    ============================================================================
    """

    @staticmethod
    def filter(li: list[Item],
               predicate: Callable[[Item], bool]) -> list[Item]:
        """
        ========================================================================
         Return Indexes of a Filtered-List by a given Condition.
         Ex: filter([11, 22], is_even) -> [1]
        ========================================================================
        """
        return [i for i, item in enumerate(li) if predicate(item)]

    @staticmethod
    def sample(li: list[Item],
               pct: int = None,
               size: int = None) -> list[Item]:
        """
        ========================================================================
         Return Random-Indexes based on given Condition, Size or Percentage.
         Ex: sample([11, 22], pct=100) -> [0, 1]
        ========================================================================
        """
        indexes = list(range(len(li)))
        return Items.sample(li=indexes, pct=pct, size=size)
