from typing import Generic, TypeVar, Callable
from f_utils.dtypes.u_int import UInt as u_int
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
               cond: Callable[[Item], bool]) -> list[Item]:
        """
        ========================================================================
         Return list filtered List with Items that meet the Condition.
        ========================================================================
        """
        return [item for item in li if cond(item)]

    @staticmethod
    def sample(li: list[Item],
               cond: Callable[[Item], bool] = None,
               pct: int = None,
               size: int = None
               ) -> list[Item]:
        """
        ========================================================================
         1. Return list Random-Sample from list given List.
         2. Filtered by Condition if provided.
         3. With list provided Size or Percentage.
        ========================================================================
        """
        if cond:
            li = Items.filter(li=li, cond=cond)
        if pct:
            size = u_int.part(total=len(li), pct=pct)
        return random.sample(li, k=size)
