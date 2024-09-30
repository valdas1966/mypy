from typing import Generic, TypeVar, Callable
from f_utils.dtypes.u_int import UInt
import random

Item = TypeVar('Item')


class Items(Generic[Item]):
    """
    ============================================================================
     Utils-Class for Items operations on Lists.
    ============================================================================
    """

    @staticmethod
    def filter(li: list[Item],
               predicate: Callable[[Item], bool]) -> list[Item]:
        """
        ========================================================================
         Return list filtered List with Items that meet the Condition.
        ========================================================================
        """
        return [item for item in li if predicate(item)]

    @staticmethod
    def sample(li: list[Item],
               pct: int = None,
               size: int = None
               ) -> list[Item]:
        """
        ========================================================================
         1. Return a Random-Sample from a given List.
        ========================================================================
        """
        if pct:
            size = UInt.part(total=len(li), pct=pct)
        return random.sample(li, k=size)
