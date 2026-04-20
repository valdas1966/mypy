from f_hs.algo.i_0_base._search_state import SearchStateSPP
from f_hs.algo.i_0_base.main import AlgoSPP
from f_hs.frontier.i_1_priority.main import FrontierPriority
from f_hs.heuristic.i_0_base._cache_entry import CacheEntry
from f_hs.heuristic.i_0_base.main import HBase
from f_hs.heuristic.i_1_bounded.main import HBounded
from f_hs.heuristic.i_1_callable.main import HCallable
from f_hs.heuristic.i_1_cached.main import HCached
from f_hs.problem.i_0_base.main import ProblemSPP
from f_hs.solution.main import SolutionSPP
from f_hs.state.i_0_base.main import StateBase
from typing import Callable, Generic, TypeVar

State = TypeVar('State', bound=StateBase)


class AStar(Generic[State], AlgoSPP[State]):
    """
    ========================================================================
     A* Search Algorithm.
    ========================================================================
    """

    # Factory
    Factory: type = None

    def __init__(self,
                 problem: ProblemSPP[State],
                 h: HBase[State] | Callable[[State], float],
                 name: str = 'AStar',
                 is_recording: bool = False,
                 search_state: SearchStateSPP[State] | None = None
                 ) -> None:
        """
        ====================================================================
         Init private Attributes.

         Accepts either an HBase subclass or a raw Callable.
         Callables are auto-wrapped in HCallable — existing call
         sites that pass a lambda keep working unchanged.

         Admissibility guard: if h is an HCached, its `goal` must
         be one of the problem's goals. A cache harvested against
         a different goal silently violates A*'s admissibility
         (cached h* to the wrong goal may over-estimate h* to the
         right one). Fail loud at init.

         `search_state` — optional pre-built SearchStateSPP; see
         `AlgoSPP.__init__` docstring. Use `resume()` (not
         `run()`) after construction to pump the seeded state.
        ====================================================================
        """
        AlgoSPP.__init__(self,
                         problem=problem,
                         frontier=FrontierPriority[State](),
                         name=name,
                         is_recording=is_recording,
                         search_state=search_state)
        self._h: HBase[State] = (h if isinstance(h, HBase)
                                 else HCallable[State](fn=h))
        if isinstance(self._h, HCached):
            if self._h.goal not in self.problem.goals:
                raise ValueError(
                    f'HCached goal {self._h.goal!r} is not a goal '
                    f'of the problem; admissibility cannot be '
                    f'guaranteed (cached h* to a different goal '
                    f'may over-estimate h* to the right goal).')

    # ──────────────────────────────────────────────────
    #  Priority / Enrichment
    # ──────────────────────────────────────────────────

    def _priority(self, state: State) -> tuple:
        """
        ====================================================================
         Priority = (f, -g, cache_rank, state). Lexicographic:
           1. f = g + h                 — lower f first.
           2. -g                        — deeper (higher-g) first.
           3. cache_rank                — cached (0) before uncached (1);
                                          a cached pop gives O(1)
                                          early-termination, strictly
                                          less work than expanding an
                                          uncached tie.
           4. state (HasKey Comparable) — deterministic fallback.

         For non-HCached heuristics, `is_perfect` is always False,
         so cache_rank is a constant 1 and the tuple collapses to
         `(f, -g, 1, state)` — behaviourally identical to the
         pre-cache `(f, -g, state)` ordering (no test drift).
        ====================================================================
        """
        g = self._search.g[state]
        f = g + self._h(state)
        cache_rank = 0 if self._h.is_perfect(state) else 1
        return (f, -g, cache_rank, state)

    def _enrich_event(self, event: dict) -> None:
        """
        ====================================================================
         Add h and f to push / pop / decrease_g events.

         On push / pop, also add:
           - `is_cached=True`  — when `self._h.is_perfect(state)`
                                 (HCached hit). The cache-hit
                                 terminator is identifiable as
                                 "the last pop carrying
                                 is_cached=True".
           - `is_bounded=True` — when `self._h.is_bounded(state)`
                                 (HBounded strictly tightened h
                                 beyond base). Visibility-only;
                                 no terminator semantics.

         Both flags are **absent** (not False) when not applicable,
         per the framework Recording Principle (no constant-False
         flags). A state can carry both flags simultaneously only
         via composition (e.g., HCached(base=HBounded)) — not
         supported in Phase 2a.

         `decrease_g` does NOT carry either flag: cache/bound
         membership was already signalled on the state's initial
         push.
        ====================================================================
        """
        t = event.get('type')
        if t in ('push', 'pop', 'decrease_g'):
            h = self._h(event['state'])
            event['h'] = h
            event['f'] = event['g'] + h
            if t in ('push', 'pop'):
                if self._h.is_perfect(event['state']):
                    event['is_cached'] = True
                if self._h.is_bounded(event['state']):
                    event['is_bounded'] = True

    # ──────────────────────────────────────────────────
    #  Early-Exit (HCached perfect-h termination)
    # ──────────────────────────────────────────────────

    def _early_exit(self, state: State) -> SolutionSPP | None:
        """
        ====================================================================
         If the heuristic is perfect at `state`, terminate
         immediately: cost = g(state) + h_perfect(state). Sets
         search_state.cache_hit.

         No event is emitted — the pop just recorded (with
         `is_cached=True` added by _enrich_event) already marks
         this state as the terminator. Mirrors goal-pop
         termination, which also emits no dedicated event.

         Only HCached returns True from is_perfect; HCallable's
         default keeps the loop going (standard A* behavior).
        ====================================================================
        """
        if not self._h.is_perfect(state):
            return None
        h_perfect = self._h(state)
        cost = self._search.g[state] + h_perfect
        self._search.cache_hit = state
        return SolutionSPP(cost=cost)

    # ──────────────────────────────────────────────────
    #  Pre-Search Pathmax Propagation (Phase 2b)
    # ──────────────────────────────────────────────────

    @staticmethod
    def _find_hbounded(h: HBase) -> 'HBounded | None':
        """
        ====================================================================
         Walk the `._base` chain searching for an HBounded
         instance. Returns the first HBounded found, or None if
         the chain terminates without one.

         Supports the locked Phase-2b shapes:
           1. `h` IS an HBounded — returned directly.
           2. `h` is HCached whose _base chain reaches HBounded.
        ====================================================================
        """
        cur: HBase | None = h
        while cur is not None:
            if isinstance(cur, HBounded):
                return cur
            cur = getattr(cur, '_base', None)
        return None

    def propagate_pathmax(self,
                          depth: int = 2
                          ) -> dict[State, float]:
        """
        ====================================================================
         Pre-search Felner-style pathmax propagation.

         Tightens admissible lower bounds at neighbors of cached
         and bounded seeds using the admissibility inequality
             h*(n) >= h*(s) - w(s, n)
         rewritten as an update rule:
             h(n) := max(h(n), h(s) - w(s, n))

         Requires an HBounded somewhere in the heuristic chain —
         that's where tightened bounds are stored. Raises
         ValueError otherwise.

         Wave 0 seeds = HCached keys UNION HBounded keys.
         Wave k (k >= 1) sources = states tightened in wave k-1.
         Terminates early when a wave tightens nothing.

         Targets exclude cached states — the cache is tighter-
         or-equal by construction; propagating into it is a
         no-op.

         `depth=0` is a valid no-op (returns {}). `depth<0`
         raises.

         No recorder events emitted (pathmax is setup, not a
         search step; mirrors `refresh_priorities`).

         Returns a cumulative dict[State, float] — every state
         whose bound was tightened, mapped to its final h value.
        ====================================================================
        """
        if depth < 0:
            raise ValueError(
                f'depth must be >= 0; got {depth!r}')
        hb = self._find_hbounded(self._h)
        if hb is None:
            raise ValueError(
                'propagate_pathmax requires an HBounded in the '
                'h chain to store propagated bounds '
                f'(self._h is {type(self._h).__name__}).')
        # Collect cached keys across the whole chain.
        cached: set[State] = set()
        cur: HBase | None = self._h
        while cur is not None:
            if isinstance(cur, HCached):
                cached.update(cur.cache.keys())
            cur = getattr(cur, '_base', None)
        # Wave 0 seeds — cached keys UNION bounded keys.
        seeds: set[State] = set(cached) | set(hb.bounds.keys())
        updates: dict[State, float] = {}
        sources: set[State] = seeds
        for _ in range(depth):
            if not sources:
                break
            next_sources: set[State] = set()
            # Sort sources for deterministic event ordering —
            # set iteration is hash-order-dependent, which would
            # make recording tests flaky across Python runs.
            for s in sorted(sources):
                h_s = self._h(s)
                for n in self.problem.successors(s):
                    if n in cached:
                        continue
                    cand = h_s - self.problem.w(parent=s,
                                                child=n)
                    if hb.add_bound(state=n, value=cand):
                        next_sources.add(n)
                        new_h = self._h(n)
                        updates[n] = new_h
                        # Emit propagate event on strict
                        # tightening (matches push/decrease_g
                        # convention — no-op attempts aren't
                        # recorded).
                        self._record_event(
                            type='propagate',
                            state=n,
                            parent=s,
                            h_parent=h_s,
                            h=new_h,
                        )
            sources = next_sources
        return updates

    # ──────────────────────────────────────────────────
    #  Cache Harvest (to feed a subsequent AStar run)
    # ──────────────────────────────────────────────────

    def to_cache(self) -> dict[State, CacheEntry[State]]:
        """
        ====================================================================
         Harvest on-path cache entries from the last completed run.

         Supports both termination modes (2026-04-20 decision):
           - Goal-pop (goal_reached set): walks start → goal,
             total_cost = g(goal). suffix_next on the goal is None.
           - Cache-hit (cache_hit set):   walks start → cache_hit,
             total_cost = g(cache_hit) + h_perfect(cache_hit).
             suffix_next on the cache_hit terminal points into
             the existing cache (so the caller can chain the
             harvest onto the prior cache without losing the
             suffix).

         Emits a CacheEntry for every state on the walked
         parent-chain:
            h_perfect[state] = total_cost - g(state)
            suffix_next      = next state on the chain (or, for
                               the terminal, the cache's own
                               suffix_next on cache-hit; None
                               on goal-pop).

         Raises ValueError if neither termination mode fired
         (e.g., unreachable goal — frontier exhausted).
        ====================================================================
        """
        terminated_by_goal = self._search.goal_reached is not None
        terminal: State | None = (self._search.goal_reached
                                  if terminated_by_goal
                                  else self._search.cache_hit)
        if terminal is None:
            raise ValueError(
                'to_cache requires a completed run; no goal '
                'reached and no cache hit.')
        total = self._search.g[terminal]
        if not terminated_by_goal:
            total += self._h(terminal)
        path = AlgoSPP.reconstruct_path(self, goal=terminal)
        out: dict[State, CacheEntry[State]] = {}
        for i, st in enumerate(path):
            if i + 1 < len(path):
                nxt: State | None = path[i + 1]
            elif terminated_by_goal:
                nxt = None
            else:
                nxt = self._h.suffix_next(terminal)
            out[st] = CacheEntry(
                h_perfect=total - self._search.g[st],
                suffix_next=nxt,
            )
        return out

    # ──────────────────────────────────────────────────
    #  Path Reconstruction (suffix-stitching on cache_hit)
    # ──────────────────────────────────────────────────

    def reconstruct_path(self,
                         goal: State | None = None
                         ) -> list[State]:
        """
        ====================================================================
         Reconstruct the Path from Start to Goal. Extends the
         base behavior: when termination was via cache_hit and no
         explicit `goal` was passed, walks parents to cache_hit
         and stitches the cached suffix onto the end (via
         HCached.suffix_next).

         Explicit `goal` argument always bypasses the stitching —
         caller is in control of the reconstruction target.
        ====================================================================
        """
        if (goal is None
                and self._search.goal_reached is None
                and self._search.cache_hit is not None):
            prefix = AlgoSPP.reconstruct_path(
                self, goal=self._search.cache_hit)
            suffix: list[State] = []
            cur = self._h.suffix_next(self._search.cache_hit)
            while cur is not None:
                suffix.append(cur)
                cur = self._h.suffix_next(cur)
            return prefix + suffix
        return AlgoSPP.reconstruct_path(self, goal=goal)
