from f_hs.algo.i_1_astar.main import AStar
from f_hs.heuristic.i_0_base._cache_entry import CacheEntry
from f_hs.heuristic.i_1_callable.main import HCallable
from f_hs.heuristic.i_1_cached.main import HCached
from f_hs.problem import ProblemSPP
from f_hs.problem.i_1_grid import ProblemGrid
from f_hs.state.i_0_base.main import StateBase


class Factory:
    """
    ========================================================================
     Factory for AStar test instances.
    ========================================================================
    """

    @staticmethod
    def graph_abc() -> AStar:
        """
        ====================================================================
         A* on linear Graph: A -> B -> C with admissible h.
        ====================================================================
        """
        h_map = {'A': 2.0, 'B': 1.0, 'C': 0.0}
        return AStar(
            problem=ProblemSPP.Factory.graph_abc(),
            h=lambda s: h_map.get(s.key, 0.0),
        )

    @staticmethod
    def graph_no_path() -> AStar:
        """
        ====================================================================
         A* on Graph with no path to goal.
        ====================================================================
        """
        return AStar(
            problem=ProblemSPP.Factory.graph_no_path(),
            h=lambda s: 0.0,
        )

    @staticmethod
    def graph_start_is_goal() -> AStar:
        """
        ====================================================================
         A* where start equals goal.
        ====================================================================
        """
        return AStar(
            problem=ProblemSPP.Factory.graph_start_is_goal(),
            h=lambda s: 0.0,
        )

    @staticmethod
    def graph_diamond() -> AStar:
        """
        ====================================================================
         A* on diamond Graph with admissible h.
        ====================================================================
        """
        h_map = {'A': 2.0, 'B': 1.0, 'C': 1.0, 'D': 0.0}
        return AStar(
            problem=ProblemSPP.Factory.graph_diamond(),
            h=lambda s: h_map.get(s.key, 0.0),
        )

    @staticmethod
    def grid_3x3() -> AStar:
        """
        ====================================================================
         A* on open 3x3 Grid with Manhattan heuristic.
        ====================================================================
        """
        problem = ProblemGrid.Factory.grid_3x3()
        goal = problem.goal
        return AStar(
            problem=problem,
            h=lambda s: float(s.distance(goal)),
        )

    @staticmethod
    def grid_3x3_obstacle() -> AStar:
        """
        ====================================================================
         A* on 3x3 Grid with obstacle, Manhattan heuristic.
        ====================================================================
        """
        problem = ProblemGrid.Factory.grid_3x3_obstacle()
        goal = problem.goal
        return AStar(
            problem=problem,
            h=lambda s: float(s.distance(goal)),
        )

    @staticmethod
    def grid_3x3_no_path() -> AStar:
        """
        ====================================================================
         A* on 3x3 Grid with wall blocking all paths.
        ====================================================================
        """
        problem = ProblemGrid.Factory.grid_3x3_no_path()
        goal = problem.goal
        return AStar(
            problem=problem,
            h=lambda s: float(s.distance(goal)),
        )

    @staticmethod
    def grid_3x3_start_is_goal() -> AStar:
        """
        ====================================================================
         A* on 3x3 Grid where start equals goal.
        ====================================================================
        """
        problem = ProblemGrid.Factory.grid_3x3_start_is_goal()
        goal = problem.goal
        return AStar(
            problem=problem,
            h=lambda s: float(s.distance(goal)),
        )

    @staticmethod
    def graph_decrease() -> AStar:
        """
        ====================================================================
         A* on the weighted decrease-graph (S -> A/B -> X with
         w(B,X) = 0) using h = 0 throughout. Reduces to Dijkstra's
         pop order — A pops before B by State tiebreak — but
         AStar's _enrich_event still adds h and f to the recorded
         decrease_g event, exercising the h/f code path on that
         event type. See ProblemSPP.Factory.graph_decrease.
        ====================================================================
        """
        return AStar(
            problem=ProblemSPP.Factory.graph_decrease(),
            h=lambda s: 0.0,
        )

    @staticmethod
    def graph_abc_cached_at_start() -> AStar:
        """
        ====================================================================
         A* on graph_abc with HCached covering ALL of {A, B, C}.
         Pop(A) immediately triggers _early_exit (is_perfect(A)
         is True) — zero expansions. Cost = g(A) + h_perfect(A)
         = 0 + 2 = 2. Path via suffix-stitching: A -> B -> C.
         Degenerate harvest case (all cache entries are inputs).
        ====================================================================
        """
        a = StateBase[str](key='A')
        b = StateBase[str](key='B')
        c = StateBase[str](key='C')
        cache = {
            a: CacheEntry(h_perfect=2.0, suffix_next=b),
            b: CacheEntry(h_perfect=1.0, suffix_next=c),
            c: CacheEntry(h_perfect=0.0, suffix_next=None),
        }
        return AStar(
            problem=ProblemSPP.Factory.graph_abc(),
            h=HCached(base=HCallable(fn=lambda s: 0.0),
                      cache=cache, goal=c),
        )

    @staticmethod
    def graph_abc_cached_at_b() -> AStar:
        """
        ====================================================================
         A* on graph_abc with HCached covering only {B, C}.
         Pop(A) is NOT perfect → expand → push(B). Pop(B)
         triggers _early_exit. Cost = g(B) + h_perfect(B) = 1 + 1
         = 2. Non-degenerate harvest case: to_cache() emits a
         new entry for A (discovered prefix) in addition to the
         entry for B (re-emitted, terminal). Base = h(A)=2.
        ====================================================================
        """
        b = StateBase[str](key='B')
        c = StateBase[str](key='C')
        cache = {
            b: CacheEntry(h_perfect=1.0, suffix_next=c),
            c: CacheEntry(h_perfect=0.0, suffix_next=None),
        }
        h_map = {'A': 2.0}
        return AStar(
            problem=ProblemSPP.Factory.graph_abc(),
            h=HCached(
                base=HCallable(fn=lambda s: h_map.get(s.key, 0.0)),
                cache=cache, goal=c),
        )

    @staticmethod
    def grid_4x4_obstacle() -> AStar:
        """
        ====================================================================
         A* on 4x4 Grid with a vertical 2-cell wall at (0,2) and
         (1,2). Start (0,0), goal (0,3). Manhattan heuristic —
         admissible but loose (it ignores the wall), so f-values
         along the detour rise above 3 and A* still explores row
         1 and row 2 before reaching the goal. Optimal cost 7.
        ====================================================================
        """
        problem = ProblemGrid.Factory.grid_4x4_obstacle()
        goal = problem.goal
        return AStar(
            problem=problem,
            h=lambda s: float(s.distance(goal)),
        )
