from f_hs.heuristic.i_0_base._cache_entry import CacheEntry
from f_hs.heuristic.i_0_base.main import HBase
from f_hs.state.i_0_base.main import StateBase
from typing import Generic, TypeVar

State = TypeVar('State', bound=StateBase)


class HCached(Generic[State], HBase[State]):
    """
    ============================================================================
     Heuristic Source backed by a frozen dict of CacheEntry rows.

     Semantics:
       - On a cached state: h := entry.h_perfect (provably tight).
       - Off a cached state: delegate to self._base.
       - is_perfect(s)  ⇔ s in the cache.
       - suffix_next(s) — entry.suffix_next on hit, else None.

     The cache is **static for the lifetime of this object**:
     the constructor takes a defensive shallow copy; no mutation
     API is exposed. Rationale: 2026-04-20 locked decision
     (static cache; growable variant deferred until a use case
     forces it — bidirectional is out of scope for Phase 1).

     `goal` records the goal this cache was harvested against.
     AStar sanity-checks membership in `problem.goals` at init
     to prevent silent admissibility violations from mis-wired
     caches.
    ============================================================================
    """

    # Factory
    Factory: type = None

    def __init__(self,
                 base: HBase[State],
                 cache: dict[State, CacheEntry[State]],
                 goal: State) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        self._base  = base
        self._cache: dict[State, CacheEntry[State]] = dict(cache)
        self._goal  = goal

    @property
    def goal(self) -> State:
        """
        ========================================================================
         The goal this cache was harvested against.
        ========================================================================
        """
        return self._goal

    @property
    def cache(self) -> dict[State, CacheEntry[State]]:
        """
        ========================================================================
         Read-only view of the cache (shallow copy).
        ========================================================================
        """
        return dict(self._cache)

    def __call__(self, state: State) -> float:
        """
        ========================================================================
         Return entry.h_perfect on a cache hit; delegate to base
         on a miss.
        ========================================================================
        """
        e = self._cache.get(state)
        return e.h_perfect if e is not None else self._base(state)

    def is_perfect(self, state: State) -> bool:
        """
        ========================================================================
         True iff the state is present in the cache.
        ========================================================================
        """
        return state in self._cache

    def suffix_next(self, state: State) -> State | None:
        """
        ========================================================================
         Return the next State on the cached optimal suffix, or
         None on a miss / when the entry is the goal itself.
        ========================================================================
        """
        e = self._cache.get(state)
        return e.suffix_next if e is not None else None
