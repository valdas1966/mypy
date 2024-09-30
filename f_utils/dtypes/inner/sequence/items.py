from typing import Generic, TypeVar, Callable, Sequence
import random

Item = TypeVar('Item')


class Items(Generic[Item]):
    """
    ============================================================================
     Utils-Class for operations on Sequences (list, tuple, str, etc.).
    ============================================================================
    """

    @staticmethod
    def filter(seq: Sequence[Item],
               predicate: Callable[[Item], bool]) -> Sequence[Item]:
        """
        ========================================================================
         Return a filtered Sequence with Items that meet the Predicate.
        ========================================================================
        """
        filtered = [item for item in seq if predicate(item)]
        return Items._return(seq=seq, li=filtered)

    @staticmethod
    def sample(seq: Sequence[Item],
               pct: int = None,
               size: int = None) -> Sequence[Item]:
        """
        ========================================================================
         Return a Random-Sample from a given Sequence.
        ========================================================================
        """
        if pct:
            size = int(len(seq) * (pct / 100))
        sampled = random.sample(seq, k=size)
        return Items._return(seq=seq, li=sampled)

    @staticmethod
    def _return(seq: Sequence[Item],
                li: list[Item]) -> Sequence[Item]:
        """
        ========================================================================
         Return the Result as a given Sequence-Type (str, tuple, list and etc.)
        ========================================================================
        """
        if isinstance(seq, str):
            return ''.join(li)
        return type(seq)(li)
