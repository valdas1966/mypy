from typing import TypeVar, Generic, Callable, Sequence
from f_utils.dtypes.inner.sequence.items import Items

Item = TypeVar('Item')


class Indexes(Generic[Item]):
    """
    ============================================================================
     Utils-Class for Indexes operations on Lists.
    ============================================================================
    """

    @staticmethod
    def filter(seq: Sequence[Item],
               predicate: Callable[[Item], bool]) -> list[int]:
        """
        ========================================================================
         Return Indexes of a Filtered-List by a given Condition.
         Ex: filter([11, 22], is_even) -> [1]
        ========================================================================
        """
        return [i for i, item in enumerate(seq) if predicate(item)]

    @staticmethod
    def sample(seq: Sequence[Item],
               pct: int = None,
               size: int = None) -> list[int]:
        """
        ========================================================================
         Return Random-Indexes based on a given Size|Pct.
         Ex: sample([11, 22], pct=100) -> [0, 1]
        ========================================================================
        """
        indexes = list(range(len(seq)))
        return list(Items.sample(seq=indexes, pct=pct, size=size))
