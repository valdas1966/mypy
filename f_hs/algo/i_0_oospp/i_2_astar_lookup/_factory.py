from f_hs.algo.i_0_oospp.i_2_astar_lookup.main import AStarLookup
from f_hs.heuristic.i_0_base._cache_entry import CacheEntry
from f_hs.problem import ProblemSPP
from f_hs.problem.i_1_grid import ProblemGrid
from f_hs.state.i_0_base.main import StateBase


class Factory:
    """
    ========================================================================
     Factory for AStarLookup test instances. Exercises the
     dict-based kwargs API (cache / goal / bounds) directly
     rather than pre-built HCached / HBounded instances; the
     parametric BPMX builders flip `rule_bpmx` / `depth_bpmx`
     to cover the in-search Felner mechanism in isolation and
     in combination with cache.
    ========================================================================
    """

    # ──────────────────────────────────────────────────
    #  Cache-only (BPMX off)
    # ──────────────────────────────────────────────────

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
    def graph_abc_cached_at_b(rule_bpmx: str | None = None,
                              depth_bpmx: int | None = 1,
                              is_recording: bool = False
                              ) -> AStarLookup:
        """
        ====================================================================
         HCached covering only {B, C}. Pop(A) not cached →
         expand → push(B). Pop(B) triggers _early_exit. Cost
         2. Non-degenerate harvest (to_cache emits A + B).

         Parametric over BPMX kwargs — defaults reproduce
         off-mode. Active mechanisms (e.g.
         `rule_bpmx='CASCADE', depth_bpmx=1, is_recording=True`)
         exercise the combined cache + BPMX path.
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
            rule_bpmx=rule_bpmx,
            depth_bpmx=depth_bpmx,
            is_recording=is_recording,
        )

    # ──────────────────────────────────────────────────
    #  No-cache BPMX (parametric on rule / depth)
    # ──────────────────────────────────────────────────

    @staticmethod
    def grid_4x4(rule_bpmx: str | None = None,
                 depth_bpmx: int | None = 1) -> AStarLookup:
        """
        ====================================================================
         AStarLookup on the canonical 4x4 obstacle grid with
         Manhattan h. Defaults (rule_bpmx=None) reproduce
         off-mode (behaviourally identical to plain AStar). See
         AStarLookup / BPMXMixin docstrings for the
         (rule_bpmx, depth_bpmx) semantics.
        ====================================================================
        """
        problem = ProblemGrid.Factory.grid_4x4_obstacle()
        goal = problem.goal
        return AStarLookup(
            problem=problem,
            h=lambda s: float(s.distance(goal)),
            rule_bpmx=rule_bpmx,
            depth_bpmx=depth_bpmx,
        )

    @staticmethod
    def graph_diamond_inconsistent_cascade() -> AStarLookup:
        """
        ====================================================================
         Diamond graph with an artificially inconsistent heuristic
         (B has h=4, others h=0) + CASCADE (full reach) so BPMX
         has something to lift. Useful for verifying lift events
         fire.
        ====================================================================
        """
        h_inc = {'A': 0.0, 'B': 4.0, 'C': 0.0, 'D': 0.0}
        return AStarLookup(
            problem=ProblemSPP.Factory.graph_diamond(),
            h=lambda s: h_inc.get(s.key, 0.0),
            rule_bpmx='CASCADE',
            depth_bpmx=None,
            is_recording=True,
        )

    # ──────────────────────────────────────────────────
    #  Bespoke cache + BPMX scenarios
    # ──────────────────────────────────────────────────

    @staticmethod
    def grid_4x4_cached_suffix_cascade_d1() -> AStarLookup:
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
        return AStarLookup(
            problem=problem,
            h=lambda s: float(s.distance(goal)),
            cache=cache,
            goal=goal,
            rule_bpmx='CASCADE',
            depth_bpmx=1,
        )
