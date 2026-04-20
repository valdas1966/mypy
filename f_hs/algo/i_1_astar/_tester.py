import pytest

from f_ds.grids.cell.i_1_map import CellMap

from f_hs.algo.i_1_astar import AStar
from f_hs.heuristic.i_0_base._cache_entry import CacheEntry
from f_hs.heuristic.i_1_bounded.main import HBounded
from f_hs.heuristic.i_1_callable.main import HCallable
from f_hs.heuristic.i_1_cached.main import HCached
from f_hs.problem import ProblemSPP
from f_hs.problem.i_1_grid import ProblemGrid
from f_hs.state.i_0_base.main import StateBase
from f_hs.state.i_1_cell.main import StateCell


def test_graph_abc_path_found() -> None:
    """
    ========================================================================
     Test AStar on A -> B -> C finds the optimal path (cost 2).
    ========================================================================
    """
    algo = AStar.Factory.graph_abc()
    solution = algo.run()
    assert bool(solution) is True
    assert solution.cost == 2.0
    path = algo.reconstruct_path()
    assert len(path) == 3
    assert path[0].key == 'A'
    assert path[-1].key == 'C'


def test_no_path() -> None:
    """
    ========================================================================
     Test AStar returns invalid when no path exists.
    ========================================================================
    """
    algo = AStar.Factory.graph_no_path()
    solution = algo.run()
    assert bool(solution) is False
    assert solution.cost == float('inf')


def test_start_is_goal() -> None:
    """
    ========================================================================
     Test AStar handles start == goal (cost 0, path length 1).
    ========================================================================
    """
    algo = AStar.Factory.graph_start_is_goal()
    solution = algo.run()
    assert bool(solution) is True
    assert solution.cost == 0.0
    path = algo.reconstruct_path()
    assert len(path) == 1
    assert path[0].key == 'A'


def test_diamond() -> None:
    """
    ========================================================================
     Test AStar on diamond graph finds optimal path (cost 2).
    ========================================================================
    """
    algo = AStar.Factory.graph_diamond()
    solution = algo.run()
    assert bool(solution) is True
    assert solution.cost == 2.0
    path = algo.reconstruct_path()
    assert len(path) == 3
    assert path[0].key == 'A'
    assert path[-1].key == 'D'


def test_elapsed() -> None:
    """
    ========================================================================
     Test elapsed time is set after run.
    ========================================================================
    """
    algo = AStar.Factory.graph_abc()
    algo.run()
    assert algo.elapsed is not None
    assert algo.elapsed >= 0


def test_search_state() -> None:
    """
    ========================================================================
     The search_state property exposes the dynamic SearchStateSPP.
     After run() it reports the goal_reached and the populated
     g / parent / closed bundle.
    ========================================================================
    """
    algo = AStar.Factory.graph_abc()
    algo.run()
    s = algo.search_state
    assert s.goal_reached is not None
    assert s.goal_reached.key == 'C'
    assert s.g[s.goal_reached] == 2.0
    assert s.parent[s.goal_reached] is not None
    assert s.parent[s.goal_reached].key == 'B'


def test_resume_preserves_state() -> None:
    """
    ========================================================================
     resume() continues the loop without re-initializing —
     closed set after run() is a subset of closed set after
     resume(), and existing g-values are preserved. Verified on
     graph_diamond, where C is pushed-but-not-popped during
     run() and gets popped during resume().
    ========================================================================
    """
    algo = AStar.Factory.graph_diamond()
    algo.run()
    closed_after_run = set(algo.search_state.closed)
    g_after_run = dict(algo.search_state.g)
    assert closed_after_run, 'closed should be populated after run'

    algo.resume()
    closed_after_resume = set(algo.search_state.closed)
    g_after_resume = dict(algo.search_state.g)
    assert closed_after_run.issubset(closed_after_resume)
    assert len(closed_after_resume) > len(closed_after_run)
    for state, g in g_after_run.items():
        assert g_after_resume[state] == g
    assert algo.elapsed is not None
    assert algo.elapsed >= 0


def test_cache_hit_early_term() -> None:
    """
    ========================================================================
     With HCached covering the start state, AStar pops A, fires
     _early_exit (is_perfect(A) is True), and returns cost = g(A)
     + h_perfect(A) = 0 + 2 = 2 without expanding B or C. The
     search_state reports cache_hit=A; goal_reached stays None.
     reconstruct_path stitches the cached suffix: A -> B -> C.
    ========================================================================
    """
    algo = AStar.Factory.graph_abc_cached_at_start()
    sol = algo.run()
    assert bool(sol) is True
    assert sol.cost == 2.0
    s = algo.search_state
    assert s.cache_hit is not None and s.cache_hit.key == 'A'
    assert s.goal_reached is None
    assert s.closed == set()   # no expansion happened
    path = algo.reconstruct_path()
    assert [p.key for p in path] == ['A', 'B', 'C']


def test_to_cache_round_trip() -> None:
    """
    ========================================================================
     Run AStar to completion on graph_abc (goal-pop path),
     harvest to_cache(), wrap it in an HCached, then run a
     fresh AStar on the same problem. The fresh run terminates
     via cache_hit on the start with the same cost (2.0),
     proving the harvest is consumable.
    ========================================================================
    """
    first = AStar.Factory.graph_abc()
    sol1 = first.run()
    assert sol1.cost == 2.0
    cache = first.to_cache()
    # graph_abc path is A -> B -> C, so harvest covers all 3.
    assert len(cache) == 3
    assert {s.key for s in cache} == {'A', 'B', 'C'}

    problem = ProblemSPP.Factory.graph_abc()
    goal = problem.goals[0]
    h = HCached(base=HCallable(fn=lambda s: 0.0),
                cache=cache, goal=goal)
    second = AStar(problem=problem, h=h)
    sol2 = second.run()
    assert sol2.cost == 2.0
    assert second.search_state.cache_hit is not None
    assert second.search_state.cache_hit.key == 'A'
    assert second.search_state.closed == set()


def test_to_cache_after_cache_hit() -> None:
    """
    ========================================================================
     Non-degenerate harvest: AStar terminates via cache_hit on B
     (cache covers only {B, C}). to_cache() emits BOTH:
       - A: newly-discovered prefix entry (h_perfect = 2.0,
            suffix_next = B).
       - B: terminal entry whose suffix_next points into the
            existing cache (= C).
     Proves the cache-hit harvest contributes the new prefix
     info and keeps the suffix chain intact — the OMSPP /
     MOSPP / MMSPP incremental-reuse idiom (2026-04-20 driver).
    ========================================================================
    """
    algo = AStar.Factory.graph_abc_cached_at_b()
    algo.run()
    assert algo.search_state.cache_hit is not None
    assert algo.search_state.cache_hit.key == 'B'

    harvested = algo.to_cache()
    by_key = {s.key: e for s, e in harvested.items()}
    assert set(by_key) == {'A', 'B'}
    assert by_key['A'].h_perfect == 2.0
    assert by_key['A'].suffix_next.key == 'B'
    assert by_key['B'].h_perfect == 1.0
    # B is terminal — its suffix_next comes from the existing
    # cache (points to C), not from a further walked prefix.
    assert by_key['B'].suffix_next.key == 'C'


def test_init_raises_on_goal_mismatch() -> None:
    """
    ========================================================================
     Passing an HCached whose goal is NOT one of the problem's
     goals must fail loud at __init__. A cache harvested against
     the wrong goal silently violates A*'s admissibility
     (cached h* to the wrong goal may over-estimate h* to the
     right one).
    ========================================================================
    """
    z = StateBase[str](key='Z')
    bad_cache = {z: CacheEntry(h_perfect=0.0, suffix_next=None)}
    h = HCached(base=HCallable(fn=lambda s: 0.0),
                cache=bad_cache, goal=z)
    with pytest.raises(ValueError, match='not a goal'):
        AStar(problem=ProblemSPP.Factory.graph_abc(), h=h)


def test_is_cached_tiebreak_picks_cached_over_uncached() -> None:
    """
    ========================================================================
     Priority = (f, -g, cache_rank, state). The cache_rank
     component prefers cached (0) over uncached (1) when f and
     -g tie. Pins that the tiebreak is load-bearing — not
     just a noop inherited from state-order.

     Construct AStar with HCached covering 'C'. Prime the
     search state with A (uncached, g=2) and C (cached, g=2)
     both on the frontier under _priority semantics. A and C
     tie on f and -g (both f=4, -g=-2 given the cache values
     below). State tiebreak would pick A (< C). The cache_rank
     tiebreak flips it — C wins and fires early-exit.
    ========================================================================
    """
    problem = ProblemSPP.Factory.graph_abc()
    a = StateBase[str](key='A')
    c = StateBase[str](key='C')
    cache = {c: CacheEntry(h_perfect=2.0, suffix_next=None)}
    h = HCached(base=HCallable(fn=lambda s: 2.0),
                cache=cache, goal=c)
    algo = AStar(problem=problem, h=h)

    # Build priority tuples DIRECTLY and verify the cached one
    # wins. We stage the g-values on the internal bundle so that
    # _priority has what it needs.
    algo._search.g[a] = 2.0
    algo._search.g[c] = 2.0
    prio_a = algo._priority(state=a)
    prio_c = algo._priority(state=c)
    # f and -g identical:
    assert prio_a[0] == prio_c[0] == 4.0     # f
    assert prio_a[1] == prio_c[1] == -2.0    # -g
    # cache_rank: cached 0 < uncached 1.
    assert prio_c[2] == 0 and prio_a[2] == 1
    # Therefore cached < uncached — min-heap picks C first.
    assert prio_c < prio_a
    # And 'A' < 'C' by state alone — the tiebreak would pick A
    # without the cache_rank. This is the load-bearing pin.
    assert prio_a[3] < prio_c[3]


def test_resume_auto_refreshes_stale_frontier_priorities() -> None:
    """
    ========================================================================
     Inject a SearchStateSPP whose frontier entry was pushed
     with a DELIBERATELY WRONG priority (computed against an
     incorrect heuristic). resume() auto-detects the dirty flag
     (set because a `search_state` was injected at __init__),
     refreshes the frontier with correct priorities, and pumps
     to the optimal solution.

     Without refresh, the wrong priority would skew pop-order
     and could break optimality or determinism in larger
     scenarios. The flag is cleared after the first refresh —
     subsequent resume() calls skip it.
    ========================================================================
    """
    from f_hs.algo.i_0_base._search_state import SearchStateSPP
    from f_hs.frontier.i_1_priority.main import FrontierPriority

    problem = ProblemSPP.Factory.graph_abc()
    a = StateBase[str](key='A')
    b = StateBase[str](key='B')

    seed = SearchStateSPP[StateBase[str]](
        frontier=FrontierPriority[StateBase[str]](),
        g={a: 0.0, b: 1.0},
        parent={a: None, b: a},
        closed={a},
    )
    # Push B with a DELIBERATELY WRONG priority — (999, 0, 1, b)
    # would place B effectively at the back of the heap if not
    # refreshed. Any correct priority should be much lower.
    seed.frontier.push(state=b, priority=(999.0, 0, 1, b))

    h_map = {'A': 2.0, 'B': 1.0, 'C': 0.0}
    algo = AStar(
        problem=problem,
        h=lambda s: h_map.get(s.key, 0.0),
        search_state=seed,
    )
    # Dirty flag set at __init__ because search_state was given.
    assert algo._frontier_dirty is True

    sol = algo.resume()
    assert sol.cost == 2.0
    # Flag cleared after first refresh.
    assert algo._frontier_dirty is False
    # Goal reached correctly despite the stale push priority —
    # refresh corrected it before pumping.
    assert algo.search_state.goal_reached is not None
    assert algo.search_state.goal_reached.key == 'C'

    # A second resume() is a no-op (frontier empty after
    # goal-pop) and does NOT re-refresh.
    algo.resume()
    assert algo._frontier_dirty is False


def test_propagate_pathmax_raises_without_hbounded() -> None:
    """
    ========================================================================
     Calling propagate_pathmax on an AStar whose h has no
     HBounded in its chain raises ValueError — no target
     storage for tightened bounds.
    ========================================================================
    """
    algo = AStar.Factory.graph_abc()   # plain HCallable
    with pytest.raises(ValueError, match='HBounded'):
        algo.propagate_pathmax(depth=2)


def test_propagate_pathmax_grid_4x4_depth_1_from_bounded_seed() -> None:
    """
    ========================================================================
     Seed HBounded on grid_4x4_obstacle with (1,1)=5. Depth=1
     propagates from (1,1) to successors (0,1), (2,1), (1,0):
       candidate = 5 - 1 = 4.
       (0,1) Manhattan=2 → 4 > 2 → tighten to 4.
       (2,1) Manhattan=4 → 4 > 4 False → no tighten.
       (1,0) Manhattan=4 → 4 > 4 False → no tighten.
     Returned dict == {(0,1): 4.0}.
    ========================================================================
    """
    def sc(r: int, c: int) -> StateCell:
        return StateCell(key=CellMap(row=r, col=c))

    problem = ProblemGrid.Factory.grid_4x4_obstacle()
    goal = problem.goal
    h = HBounded(
        base=HCallable(fn=lambda s: float(s.distance(goal))),
        bounds={sc(1, 1): 5.0},
    )
    algo = AStar(problem=problem, h=h)
    updates = algo.propagate_pathmax(depth=1)
    assert updates == {sc(0, 1): 4.0}
    # Verify the bound landed.
    assert h(sc(0, 1)) == 4.0
    assert h.is_bounded(state=sc(0, 1)) is True
    # (2,1) and (1,0) untouched by propagation.
    assert h.is_bounded(state=sc(2, 1)) is False
    assert h.is_bounded(state=sc(1, 0)) is False


def test_propagate_pathmax_grid_4x4_depth_2_compounds() -> None:
    """
    ========================================================================
     Depth=2 from seed (1,1)=5 on grid_4x4_obstacle:
       Wave 1: tightens (0,1) to 4.
       Wave 2: source={(0,1)}. Successors (1,1), (0,0).
               h((0,1)) = 4. candidate = 4 - 1 = 3.
               - To (1,1): h=5 (seed). 3 > 5 False → no update.
               - To (0,0): Manhattan=3. 3 > 3 False → no update.
       Final updates == {(0,1): 4.0} — same as depth=1. Pins
       strict-monotone termination on this seed.
    ========================================================================
    """
    def sc(r: int, c: int) -> StateCell:
        return StateCell(key=CellMap(row=r, col=c))

    problem = ProblemGrid.Factory.grid_4x4_obstacle()
    goal = problem.goal
    h = HBounded(
        base=HCallable(fn=lambda s: float(s.distance(goal))),
        bounds={sc(1, 1): 5.0},
    )
    algo = AStar(problem=problem, h=h)
    updates = algo.propagate_pathmax(depth=2)
    assert updates == {sc(0, 1): 4.0}
    # Wave 2 was a no-op — (0,0) and (1,1) unchanged.
    assert h(sc(0, 0)) == 3.0   # Manhattan, unchanged
    assert h.is_bounded(state=sc(0, 0)) is False
    assert h(sc(1, 1)) == 5.0   # seed, unchanged


def test_astar_with_hbounded_finds_optimal_cost() -> None:
    """
    ========================================================================
     AStar on grid_4x4_obstacle with Manhattan wrapped in
     HBounded — bound (1,0) at h=6 (tight; h*((1,0))=6) and
     (2,0) at h=5 (tight; h*((2,0))=5). Bounds prune the high-g
     side of the wall. Asserts:
       1. Optimal cost 7 preserved (admissibility held).
       2. Bounded pop count ≤ un-bounded baseline (pruning
          doesn't hurt).
    ========================================================================
    """
    def sc(r: int, c: int) -> StateCell:
        return StateCell(key=CellMap(row=r, col=c))

    # Baseline: un-bounded Manhattan pop count.
    problem_b = ProblemGrid.Factory.grid_4x4_obstacle()
    goal_b = problem_b.goal
    base_algo = AStar(
        problem=problem_b,
        h=lambda s: float(s.distance(goal_b)),
        is_recording=True,
    )
    base_algo.run()
    base_pops = sum(1 for e in base_algo.recorder.events
                    if e.get('type') == 'pop')

    # Bounded run.
    problem = ProblemGrid.Factory.grid_4x4_obstacle()
    goal = problem.goal
    bounds = {sc(1, 0): 6.0, sc(2, 0): 5.0}
    h = HBounded(
        base=HCallable(fn=lambda s: float(s.distance(goal))),
        bounds=bounds,
    )
    algo = AStar(problem=problem, h=h, is_recording=True)
    sol = algo.run()
    assert sol.cost == 7.0

    bounded_pops = sum(1 for e in algo.recorder.events
                       if e.get('type') == 'pop')
    assert bounded_pops <= base_pops
