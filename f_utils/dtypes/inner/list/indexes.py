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
    def filter(li: list[Item], cond: Callable[[Item], bool]) -> list[Item]:
        """
        ========================================================================
         Return Indexes of a Filtered-List by a given Condition.
        ========================================================================
        """
        return [i for i, item in enumerate(li) if cond(item)]

    @staticmethod
    def sample(li: list[Item],
               cond: Callable[[Item], bool] = None,
               pct: int = None,
               size: int = None) -> list[Item]:
        """
        ========================================================================
         Return Random-Indexes based on given Condition, Size or Percentage.
        ========================================================================
        """
        indexes = Indexes.filter(li, cond) if cond else list(range(len(li)))
        return Items.sample(li=indexes, pct=pct, size=size)
