import random
from typing import Generic, TypeVar, Callable

I = TypeVar('I')

class WrapperList(Generic[I]):
    """
    ============================================================================
     Wrapper-Class for List-BuiltIn.
    ============================================================================
    """

    def __init__(self, li: list[I]) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        self._li = li

    def all(self,
            is_spec: Callable[[I], bool] = None) -> list[I]:
        """
        ========================================================================
         1. Return List with Items that corresponds to specific condition.
         2. If there is no condition, return full list.
        ========================================================================
        """
        if is_spec:
            return [x for x in self._li if is_spec(x)]
        return self._li

    def random_by_size(self,
                       size: int,
                       is_spec: Callable[[I], bool]) -> list[I]:
        """
        ========================================================================
         1. Return random list of items that meet specific conditions.
         2. If there is no condition - return random list.
        ========================================================================
        """
        li = self.all(is_spec=is_spec)
        return random.sample(li, k=size)

    def random_by_pct(self,
                      pct: int,
                      is_spec: Callable[[I], bool]) -> list[I]:
        """
        ========================================================================
         1. Return random list of items that meet specific conditions.
         2. If there is no condition - return random list.
        ========================================================================
        """
        li = self.all(is_spec=is_spec)
        size = int(pct * len(li) / 100)
        return random.sample(li, k=size)
