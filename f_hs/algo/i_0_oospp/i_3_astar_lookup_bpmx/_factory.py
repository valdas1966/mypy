from f_hs.algo.i_0_oospp.i_3_astar_lookup_bpmx.main import AStarLookupBPMX
from f_hs.heuristic.i_0_base._cache_entry import CacheEntry
from f_hs.problem import ProblemSPP
from f_hs.problem.i_1_grid import ProblemGrid
from f_hs.state.i_0_base.main import StateBase


class Factory:
    """
    ============================================================================
     Factory for AStarLookupBPMX test instances. Spans the
     three new combinations the integrated class enables:
       - cache only (BPMX off)        ≡ AStarLookup behavior.
       - BPMX only (no cache)         ≡ AStarBPMX behavior.
       - cache + BPMX                 the new path.
    ============================================================================
    """

    # ──────────────────────────────────────────────────
    #  Cache-only (BPMX off — must match AStarLookup)
    # ──────────────────────────────────────────────────

    @staticmethod
    def graph_abc_cached_at_b_off() -> AStarLookupBPMX:
        """
        ====================================================================
         Cache covering {B, C}; BPMX off. Equivalence target:
         AStarLookup's `graph_abc_cached_at_b()`.
        ====================================================================
        """
        b = StateBase[str](key='B')
        c = StateBase[str](key='C')
        cache = {
            b: CacheEntry(h_perfect=1, suffix_next=c),
            c: CacheEntry(h_perfect=0, suffix_next=None),
        }
        h_map = {'A': 2}
        return AStarLookupBPMX(
            problem=ProblemSPP.Factory.graph_abc(),
            h=lambda s: h_map.get(s.key, 0),
            cache=cache,
            goal=c,
            rule_pathmax=None,
            depth_bpmx=0,
        )

    # ──────────────────────────────────────────────────
    #  BPMX-only (no cache — must match AStarBPMX)
    # ──────────────────────────────────────────────────

    @staticmethod
    def grid_4x4_bpmx_full_no_cache() -> AStarLookupBPMX:
        """
        ====================================================================
         BPMX(infinity), no cache. Equivalence target: AStarBPMX's
         `grid_4x4_bpmx_full()` — same expansion order, same
         counters (modulo the 10-counter shape).
        ====================================================================
        """
        problem = ProblemGrid.Factory.grid_4x4_obstacle()
        goal = problem.goal
        return AStarLookupBPMX(
            problem=problem,
            h=lambda s: float(s.distance(goal)),
            rule_pathmax=None,
            depth_bpmx=None,
        )

    @staticmethod
    def grid_4x4_rule3_no_cache() -> AStarLookupBPMX:
        """
        ====================================================================
         Felner Rule 3 only, no cache. Mirrors
         `AStarBPMX.Factory.grid_4x4_rule3()`.
        ====================================================================
        """
        problem = ProblemGrid.Factory.grid_4x4_obstacle()
        goal = problem.goal
        return AStarLookupBPMX(
            problem=problem,
            h=lambda s: float(s.distance(goal)),
            rule_pathmax=3,
            depth_bpmx=0,
        )

    # ──────────────────────────────────────────────────
    #  Combined (cache + BPMX) — the new functionality
    # ──────────────────────────────────────────────────

    @staticmethod
    def graph_abc_cached_at_b_bpmx_d1() -> AStarLookupBPMX:
        """
        ====================================================================
         Cache covering {B, C} + BPMX(1). Pop(A) does NOT
         early-exit (A not cached); BPMX(1) cascade runs over
         A's neighbourhood; Pop(B) early-exits via HCached.
         Tests cache + BPMX coexisting in a single search.
        ====================================================================
        """
        b = StateBase[str](key='B')
        c = StateBase[str](key='C')
        cache = {
            b: CacheEntry(h_perfect=1, suffix_next=c),
            c: CacheEntry(h_perfect=0, suffix_next=None),
        }
        h_map = {'A': 2}
        return AStarLookupBPMX(
            problem=ProblemSPP.Factory.graph_abc(),
            h=lambda s: h_map.get(s.key, 0),
            cache=cache,
            goal=c,
            rule_pathmax=None,
            depth_bpmx=1,
            is_recording=True,
        )

    @staticmethod
    def grid_4x4_cached_suffix_bpmx_d1() -> AStarLookupBPMX:
        """
        ====================================================================
         4x4 obstacle grid with a small cached suffix near the
         goal + BPMX(1). Exercises (a) cache-hit early term
         when a cached state is popped, (b) BPMX cascade
         skipping cached descendants from lift mutation.
        ====================================================================
        """
        problem = ProblemGrid.Factory.grid_4x4_obstacle()
        goal = problem.goal
        # Cache the goal itself (h*=0) so any BPMX cascade
        # touching the goal sees it as cached / skipped from
        # lift attempts.
        cache = {goal: CacheEntry(h_perfect=0, suffix_next=None)}
        return AStarLookupBPMX(
            problem=problem,
            h=lambda s: float(s.distance(goal)),
            cache=cache,
            goal=goal,
            rule_pathmax=None,
            depth_bpmx=1,
        )

    @staticmethod
    def graph_diamond_inconsistent_bpmx_full() -> AStarLookupBPMX:
        """
        ====================================================================
         Diamond graph with artificially inconsistent h
         (B has h=4) + BPMX(infinity). Useful for verifying
         lift events fire under the combined class.
        ====================================================================
        """
        h_inc = {'A': 0.0, 'B': 4.0, 'C': 0.0, 'D': 0.0}
        return AStarLookupBPMX(
            problem=ProblemSPP.Factory.graph_diamond(),
            h=lambda s: h_inc.get(s.key, 0.0),
            rule_pathmax=None,
            depth_bpmx=None,
            is_recording=True,
        )
