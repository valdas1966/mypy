from f_core.mixins.comparable.main import Comparable
from f_core.protocols.comparison import SupportsComparison


class KeyRate(Comparable):
    """
    ============================================================================
     One key's positive/negative tally and positive rate.

     `item` : the key, taken from the union of two counters.
     `pos`  : its count in the positive counter (0 if absent).
     `neg`  : its count in the negative counter (0 if absent).
     `rate` : pos / (pos + neg); None when pos + neg == 0.

     The counter key is exposed as `item` (not `key`) because
     `key` is reserved by the Equatable/Comparable mixins for
     the comparison surrogate.

     Ordering (Comparable): higher rate first; ties broken by
     larger total (pos + neg); a None rate sorts lowest.
     Equality (Equatable): same rate, total and item.
    ============================================================================
    """

    # Factory
    Factory: type = None

    def __init__(self,
                 item: object,
                 pos: int,
                 neg: int) -> None:
        """
        ========================================================================
         Init private Attributes. `rate` is derived so an
          inconsistent (rate, pos, neg) triple cannot exist.
        ========================================================================
        """
        self._item = item
        self._pos = pos
        self._neg = neg
        total = pos + neg
        self._rate: float | None = pos / total if total else None

    @property
    def item(self) -> object:
        """
        ========================================================================
         Get the key (taken from the counters).
        ========================================================================
        """
        return self._item

    @property
    def pos(self) -> int:
        """
        ========================================================================
         Get the count in the positive counter.
        ========================================================================
        """
        return self._pos

    @property
    def neg(self) -> int:
        """
        ========================================================================
         Get the count in the negative counter.
        ========================================================================
        """
        return self._neg

    @property
    def total(self) -> int:
        """
        ========================================================================
         Get pos + neg (the combined count across both counters).
        ========================================================================
        """
        return self._pos + self._neg

    @property
    def rate(self) -> float | None:
        """
        ========================================================================
         Get pos / (pos + neg); None when the total is 0.
        ========================================================================
        """
        return self._rate

    @property
    def key(self) -> SupportsComparison:
        """
        ========================================================================
         Comparison/equality surrogate: (has-rate, rate, total,
          item-repr). Higher rate then larger total rank higher;
          a None rate ranks lowest. `repr(item)` is the final,
          type-safe tie-breaker for a total order.
        ========================================================================
        """
        rated = self._rate is not None
        rate = self._rate if rated else 0.0
        return rated, rate, self.total, repr(self._item)

    def __str__(self) -> str:
        """
        ========================================================================
         Get the string representation of the KeyRate.
        ========================================================================
        """
        rate = 'None' if self._rate is None else f'{self._rate:.3f}'
        return (f'{self._item!r}: '
                f'+{self._pos}/-{self._neg} -> {rate}')

    def __repr__(self) -> str:
        """
        ========================================================================
         Get the repr representation of the KeyRate.
        ========================================================================
        """
        return f'<KeyRate {str(self)}>'
