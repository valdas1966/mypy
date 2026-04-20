from f_hs.heuristic.i_0_base._cache_entry import CacheEntry
from f_hs.heuristic.i_1_callable.main import HCallable
from f_hs.heuristic.i_1_cached.main import HCached
from f_hs.state.i_0_base.main import StateBase


class Factory:
    """
    ========================================================================
     Factory for HCached test instances.
    ========================================================================
    """

    @staticmethod
    def graph_abc_full() -> HCached[StateBase[str]]:
        """
        ====================================================================
         HCached covering every state on A -> B -> C with the
         h*-perfect values: A=2, B=1, C=0. suffix_next traces
         the optimal path. Base = h=0 (so off-cache delegation
         returns 0 — visibly different from cached values).
        ====================================================================
        """
        a, b, c = (StateBase[str](key=k) for k in 'ABC')
        cache = {
            a: CacheEntry(h_perfect=2.0, suffix_next=b),
            b: CacheEntry(h_perfect=1.0, suffix_next=c),
            c: CacheEntry(h_perfect=0.0, suffix_next=None),
        }
        return HCached(base=HCallable(fn=lambda s: 0.0),
                       cache=cache, goal=c)

    @staticmethod
    def graph_abc_partial() -> HCached[StateBase[str]]:
        """
        ====================================================================
         Cache covers only B and C. State A misses the cache and
         delegates to the base callable (which returns 2.0 for A,
         and a sentinel 99.0 for B/C — never reached because
         B and C are cached).
        ====================================================================
        """
        b, c = (StateBase[str](key=k) for k in 'BC')
        cache = {
            b: CacheEntry(h_perfect=1.0, suffix_next=c),
            c: CacheEntry(h_perfect=0.0, suffix_next=None),
        }
        h_map = {'A': 2.0, 'B': 99.0, 'C': 99.0}
        return HCached(
            base=HCallable(fn=lambda s: h_map.get(s.key, 0.0)),
            cache=cache,
            goal=c,
        )
