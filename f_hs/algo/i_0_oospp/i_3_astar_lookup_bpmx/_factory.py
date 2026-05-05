from f_hs.algo.i_0_oospp.i_3_astar_lookup_bpmx.main import AStarLookupBPMX
from f_hs.heuristic.i_0_base._cache_entry import CacheEntry
from f_hs.problem import ProblemSPP
from f_hs.problem.i_1_grid import ProblemGrid
from f_hs.state.i_0_base.main import StateBase


class Factory:
    """
    ============================================================================
     Factory for AStarLookupBPMX test instances. Spans the
     three combinations the integrated class enables:
       - cache only (BPMX off)        ≡ AStarLookup behavior.
       - BPMX only (no cache)         ≡ AStarBPMX behavior.
       - cache + BPMX                 the integrated path.

     Both grid_4x4-no-cache and graph_abc-cached-at-b are
     parametric over `(rule_bpmx, depth_bpmx)` — defaults
     reproduce off-mode. Other cache-bearing scenarios are
     bespoke (each wires a distinct cache shape).
    ============================================================================
    """

    # ──────────────────────────────────────────────────
    #  Cache + BPMX on graph_abc (cache at B);
    #  parametric over (rule_bpmx, depth_bpmx).
    # ──────────────────────────────────────────────────

    @staticmethod
    def graph_abc_cached_at_b(rule_bpmx: str | None = None,
                              depth_bpmx: int | None = 1,
                              is_recording: bool = False
                              ) -> AStarLookupBPMX:
        """
        ====================================================================
         AStarLookupBPMX on graph_abc with cache covering
         {B, C} and h={A: 2}. Defaults reproduce off-mode
         (≡ AStarLookup's `graph_abc_cached_at_b()`); any
         active mechanism (e.g. `rule_bpmx='CASCADE'`,
         `depth_bpmx=1`) exercises the combined cache + BPMX
         path. Pop(A) does NOT early-exit (A not cached);
         Pop(B) early-exits via HCached.
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
            rule_bpmx=rule_bpmx,
            depth_bpmx=depth_bpmx,
            is_recording=is_recording,
        )

    # ──────────────────────────────────────────────────
    #  BPMX-only (no cache — must match AStarBPMX);
    #  parametric over (rule_bpmx, depth_bpmx).
    # ──────────────────────────────────────────────────

    @staticmethod
    def grid_4x4_no_cache(rule_bpmx: str | None = None,
                          depth_bpmx: int | None = 1
                          ) -> AStarLookupBPMX:
        """
        ====================================================================
         AStarLookupBPMX on the canonical 4x4 obstacle grid with
         Manhattan h, no cache. Defaults reproduce off-mode.
         Mirrors `AStarBPMX.Factory.grid_4x4(...)` for the
         no-cache equivalence side of the integration tests.
        ====================================================================
        """
        problem = ProblemGrid.Factory.grid_4x4_obstacle()
        goal = problem.goal
        return AStarLookupBPMX(
            problem=problem,
            h=lambda s: float(s.distance(goal)),
            rule_bpmx=rule_bpmx,
            depth_bpmx=depth_bpmx,
        )

    # ──────────────────────────────────────────────────
    #  Other cache + BPMX scenarios (bespoke cache shapes)
    # ──────────────────────────────────────────────────

    @staticmethod
    def grid_4x4_cached_suffix_cascade_d1() -> AStarLookupBPMX:
        """
        ====================================================================
         4x4 obstacle grid with a small cached suffix near the
         goal + CASCADE depth=1. Exercises (a) cache-hit early
         term when a cached state is popped, (b) cascade
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
            rule_bpmx='CASCADE',
            depth_bpmx=1,
        )

    @staticmethod
    def graph_diamond_inconsistent_cascade() -> AStarLookupBPMX:
        """
        ====================================================================
         Diamond graph with artificially inconsistent h
         (B has h=4) + CASCADE (full reach). Useful for
         verifying lift events fire under the combined class.
        ====================================================================
        """
        h_inc = {'A': 0.0, 'B': 4.0, 'C': 0.0, 'D': 0.0}
        return AStarLookupBPMX(
            problem=ProblemSPP.Factory.graph_diamond(),
            h=lambda s: h_inc.get(s.key, 0.0),
            rule_bpmx='CASCADE',
            depth_bpmx=None,
            is_recording=True,
        )
