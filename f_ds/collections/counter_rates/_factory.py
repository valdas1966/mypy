from collections import Counter

from f_ds.collections.counter_rates.main import CounterRates


class Factory:
    """
    ========================================================================
     Factory for the CounterRates class.
    ========================================================================
    """

    @staticmethod
    def a() -> CounterRates:
        """
        ====================================================================
         Canonical CounterRates over shared/positive-only/
          negative-only keys.
        ====================================================================
        """
        return CounterRates(positive=Counter(a=3, b=1, c=4),
                             negative=Counter(a=1, b=3, d=2))

    @staticmethod
    def empty() -> CounterRates:
        """
        ====================================================================
         CounterRates over two empty counters (no rows).
        ====================================================================
        """
        return CounterRates(positive=Counter(),
                             negative=Counter())
