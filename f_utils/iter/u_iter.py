from typing import Iterable, TypeVar
import random

Item = TypeVar('Item')

def sample(data: Iterable[Item],
           size: int = None,
           pct: int = None) -> list[Item]:
    """
    ============================================================================
     Return a random sample of the iterable.
    ============================================================================
    """
    data = list(data)
    if not size:
        size = int(len(data) * pct / 100)
    return random.sample(population=data, k=size)
