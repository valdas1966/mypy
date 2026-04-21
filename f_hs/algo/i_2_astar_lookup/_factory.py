from f_hs.algo.i_2_astar_lookup.main import AStarLookup
from f_hs.heuristic.i_0_base._cache_entry import CacheEntry
from f_hs.problem import ProblemSPP
from f_hs.state.i_0_base.main import StateBase


class Factory:
    """
    ========================================================================
     Factory for AStarLookup test instances. Exercises the
     dict-based kwargs API (cache / goal / bounds) directly
     rather than pre-built HCached / HBounded instances.
    ========================================================================
    """

    @staticmethod
    def graph_abc_cached_at_start() -> AStarLookup:
        """
        ====================================================================
         HCached covering ALL of {A, B, C}. Pop(A) immediately
         triggers _early_exit. Cost 2 via 0-expansion early
         term. Path via suffix stitch: A -> B -> C.
        ====================================================================
        """
        a = StateBase[str](key='A')
        b = StateBase[str](key='B')
        c = StateBase[str](key='C')
        cache = {
            a: CacheEntry(h_perfect=2, suffix_next=b),
            b: CacheEntry(h_perfect=1, suffix_next=c),
            c: CacheEntry(h_perfect=0, suffix_next=None),
        }
        return AStarLookup(
            problem=ProblemSPP.Factory.graph_abc(),
            h=lambda s: 0,
            cache=cache,
            goal=c,
        )

    @staticmethod
    def graph_abc_cached_at_b() -> AStarLookup:
        """
        ====================================================================
         HCached covering only {B, C}. Pop(A) not cached →
         expand → push(B). Pop(B) triggers _early_exit. Cost
         2. Non-degenerate harvest (to_cache emits A + B).
        ====================================================================
        """
        b = StateBase[str](key='B')
        c = StateBase[str](key='C')
        cache = {
            b: CacheEntry(h_perfect=1, suffix_next=c),
            c: CacheEntry(h_perfect=0, suffix_next=None),
        }
        h_map = {'A': 2}
        return AStarLookup(
            problem=ProblemSPP.Factory.graph_abc(),
            h=lambda s: h_map.get(s.key, 0),
            cache=cache,
            goal=c,
        )
