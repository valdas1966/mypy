from collections import Counter
from typing import Iterator

from f_core.mixins.equatable.main import Equatable
from f_core.protocols.equality.main import SupportsEquality
from f_ds.rates.item_rate.main import ItemRate


class CounterRates(Equatable):
    """
    ============================================================================
     Per-key positive rate built from two counters.

     For every key in the union of `positive` and `negative`,
      holds an ItemRate(item, pos, neg, rate). Binary by
      construction: the rate pos / (pos + neg) is a two-class
      quantity, so exactly two counters are accepted.

     Rows are kept sorted: higher rate first; ties broken by
      larger total (pos + neg); None-rate rows last.

     Zero guard: a key whose total is 0 gets rate None instead
      of raising. Assumes non-negative counts (the Counter
      contract). Empty inputs -> no rows.
    ============================================================================
    """

    # Factory
    Factory: type = None

    def __init__(self,
                 positive: Counter,
                 negative: Counter) -> None:
        """
        ========================================================================
         Build and sort the ItemRate rows from both counters.
        ========================================================================
        """
        keys = positive.keys() | negative.keys()
        rows = [ItemRate(item=k,
                         pos=positive.get(k, 0),
                         neg=negative.get(k, 0))
                for k in keys]
        # Comparable ranks higher rate / larger total first;
        # reverse gives descending order, None-rate rows last.
        rows.sort(reverse=True)
        self._rows: tuple[ItemRate, ...] = tuple(rows)

    @property
    def rows(self) -> tuple[ItemRate, ...]:
        """
        ========================================================================
         Get the sorted ItemRate rows.
        ========================================================================
        """
        return self._rows

    @property
    def key(self) -> SupportsEquality:
        """
        ========================================================================
         Equality surrogate: the ordered tuple of rows. Two
          CounterRates are equal iff they hold the same rows
          in the same order.
        ========================================================================
        """
        return self._rows

    def top(self, n: int) -> list[ItemRate]:
        """
        ========================================================================
         Return the `n` highest-rate rows (already sorted).
        ========================================================================
        """
        return list(self._rows[:n])

    def __len__(self) -> int:
        """
        ========================================================================
         Number of rows (distinct keys across both counters).
        ========================================================================
        """
        return len(self._rows)

    def __iter__(self) -> Iterator[ItemRate]:
        """
        ========================================================================
         Iterate the rows in sorted order.
        ========================================================================
        """
        return iter(self._rows)

    def __repr__(self) -> str:
        """
        ========================================================================
         Get the repr representation of the CounterRates.
        ========================================================================
        """
        return f'<CounterRates n={len(self._rows)}>'
