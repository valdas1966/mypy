from f_ds.grids.cell.i_1_map import CellMap
from f_ds.grids.grid.map import GridMap

from f_hs.algo.i_0_base._search_state import SearchStateSPP
from f_hs.algo.i_1_astar import AStar
from f_hs.frontier.i_1_priority.main import FrontierPriority
from f_hs.heuristic.i_0_base._cache_entry import CacheEntry
from f_hs.heuristic.i_1_bounded.main import HBounded
from f_hs.heuristic.i_1_callable.main import HCallable
from f_hs.heuristic.i_1_cached.main import HCached
from f_hs.problem import ProblemSPP
from f_hs.problem.i_1_grid import ProblemGrid
from f_hs.state.i_0_base.main import StateBase
from f_hs.state.i_1_cell.main import StateCell


def _key_of(state) -> object:
    """
    ========================================================================
     Return a comparable Key for a State.
     Graph states (key=str) return the string as-is.
     Grid states (key=CellMap) return a (row, col) tuple.
    ========================================================================
    """
    k = state.key
    if hasattr(k, 'row') and hasattr(k, 'col'):
        return (k.row, k.col)
    return k


def _normalize(event: dict) -> dict:
    """
    ========================================================================
     Return a comparable copy of an Event:
     - duration removed (non-deterministic timing)
     - state and parent unwrapped to their keys
     Dict comparison then checks the exact keyset — a pop event
     accidentally carrying a parent key would fail the test.
    ========================================================================
    """
    out = {k: v for k, v in event.items() if k != 'duration'}
    out['state'] = _key_of(event['state'])
    if 'parent' in event:
        p = event['parent']
        out['parent'] = _key_of(p) if p is not None else None
    return out


def test_recording_full_event_sequence_on_graph_abc() -> None:
    """
    ========================================================================
     Assert the exact recorded event sequence for AStar on
     A -> B -> C with admissible h = {A:2, B:1, C:0}. Every event
     carries h and f (via AStar._enrich_event), f = g + h holds
     at each event, and pop events do NOT carry a parent key.
    ========================================================================
    """
    h_map = {'A': 2.0, 'B': 1.0, 'C': 0.0}
    algo = AStar(problem=ProblemSPP.Factory.graph_abc(),
                 h=lambda s: h_map.get(s.key, 0.0),
                 is_recording=True)
    algo.run()
    actual = [_normalize(e) for e in algo.recorder.events]
    expected = [
        {'type': 'push', 'state': 'A', 'g': 0, 'parent': None, 'h': 2.0, 'f': 2.0},
        {'type': 'pop',  'state': 'A', 'g': 0, 'h': 2.0, 'f': 2.0},
        {'type': 'push', 'state': 'B', 'g': 1, 'parent': 'A', 'h': 1.0, 'f': 2.0},
        {'type': 'pop',  'state': 'B', 'g': 1, 'h': 1.0, 'f': 2.0},
        {'type': 'push', 'state': 'C', 'g': 2, 'parent': 'B', 'h': 0.0, 'f': 2.0},
        {'type': 'pop',  'state': 'C', 'g': 2, 'h': 0.0, 'f': 2.0},
    ]
    assert actual == expected


def test_recording_full_event_sequence_on_graph_diamond() -> None:
    """
    ========================================================================
     Assert the exact recorded event sequence for AStar on the
     diamond graph A -> {B, C} -> D with h = {A:2, B:1, C:1, D:0}.
     B and C share the same priority (f=2, -g=-1) — the third
     priority element (State, Comparable via HasKey) breaks the
     tie deterministically ('B' < 'C'), so B is popped first and
     the goal D is reached via B without ever expanding C.
    ========================================================================
    """
    h_map = {'A': 2.0, 'B': 1.0, 'C': 1.0, 'D': 0.0}
    algo = AStar(problem=ProblemSPP.Factory.graph_diamond(),
                 h=lambda s: h_map.get(s.key, 0.0),
                 is_recording=True)
    algo.run()
    actual = [_normalize(e) for e in algo.recorder.events]
    expected = [
        {'type': 'push', 'state': 'A', 'g': 0, 'parent': None, 'h': 2.0, 'f': 2.0},
        {'type': 'pop',  'state': 'A', 'g': 0, 'h': 2.0, 'f': 2.0},
        {'type': 'push', 'state': 'B', 'g': 1, 'parent': 'A', 'h': 1.0, 'f': 2.0},
        {'type': 'push', 'state': 'C', 'g': 1, 'parent': 'A', 'h': 1.0, 'f': 2.0},
        {'type': 'pop',  'state': 'B', 'g': 1, 'h': 1.0, 'f': 2.0},
        {'type': 'push', 'state': 'D', 'g': 2, 'parent': 'B', 'h': 0.0, 'f': 2.0},
        {'type': 'pop',  'state': 'D', 'g': 2, 'h': 0.0, 'f': 2.0},
    ]
    assert actual == expected
    # C pushed but never popped — goal D was reached via B first.
    popped = [e['state'] for e in actual if e['type'] == 'pop']
    assert 'C' not in popped


def test_recording_full_event_sequence_on_graph_decrease() -> None:
    """
    ========================================================================
     Assert the exact recorded event sequence for AStar on the
     weighted decrease-graph (S -> A/B -> X with w(B,X) = 0)
     using h = 0 throughout. A and B tie on (f=1, -g=-1); State
     tiebreak ('A' < 'B') pops A first; A pushes X with g=2;
     B pops next and re-parents X via `decrease_g` (new_g = 1).

     Pins, beyond the existing AStar tests:
       1. The `decrease_g` event type is emitted.
       2. AStar's `_enrich_event` runs on `decrease_g` too —
          the event carries `h` and `f`, not just `state` / `g`
          / `parent`.
       3. The `parent` and `g` on `decrease_g` reflect the NEW
          values (B, 1), not the previous ones (A, 2).
       4. f = g + h holds on the decrease_g event.
    ========================================================================
    """
    algo = AStar.Factory.graph_decrease()
    algo._recorder.is_active = True
    sol = algo.run()
    assert sol.cost == 1.0
    actual = [_normalize(e) for e in algo.recorder.events]
    expected = [
        {'type': 'push', 'state': 'S', 'g': 0, 'parent': None, 'h': 0.0, 'f': 0.0},
        {'type': 'pop',  'state': 'S', 'g': 0, 'h': 0.0, 'f': 0.0},
        {'type': 'push', 'state': 'A', 'g': 1, 'parent': 'S', 'h': 0.0, 'f': 1.0},
        {'type': 'push', 'state': 'B', 'g': 1, 'parent': 'S', 'h': 0.0, 'f': 1.0},
        {'type': 'pop',  'state': 'A', 'g': 1, 'h': 0.0, 'f': 1.0},
        {'type': 'push', 'state': 'X', 'g': 2, 'parent': 'A', 'h': 0.0, 'f': 2.0},
        {'type': 'pop',  'state': 'B', 'g': 1, 'h': 0.0, 'f': 1.0},
        {'type': 'decrease_g', 'state': 'X', 'g': 1, 'parent': 'B', 'h': 0.0, 'f': 1.0},
        {'type': 'pop',  'state': 'X', 'g': 1, 'h': 0.0, 'f': 1.0},
    ]
    assert actual == expected
    # Exactly one decrease_g; carries enriched h/f; new parent/g.
    decrs = [e for e in actual if e['type'] == 'decrease_g']
    assert len(decrs) == 1
    assert decrs[0]['parent'] == 'B'
    assert decrs[0]['g'] == 1
    assert decrs[0]['h'] == 0.0
    assert decrs[0]['f'] == decrs[0]['g'] + decrs[0]['h']


def test_recording_full_event_sequence_on_grid_3x3() -> None:
    """
    ========================================================================
     Assert the exact recorded event sequence for AStar on an open
     3x3 grid from (0,0) to (2,2) with Manhattan heuristic. Every
     state on the path has f = 4 (tight admissible heuristic), so
     (f,-g) ties are common — the State tiebreak picks the
     lexicographically smaller (row,col). Informed-search result:
     6 pushes + 6 pops (vs. BFS's 9+9).
    ========================================================================
    """
    problem = ProblemGrid.Factory.grid_3x3()
    goal = problem.goal
    algo = AStar(problem=problem,
                 h=lambda s: float(s.distance(goal)),
                 is_recording=True)
    algo.run()
    actual = [_normalize(e) for e in algo.recorder.events]
    expected = [
        {'type': 'push', 'state': (0, 0), 'g': 0,
         'parent': None, 'h': 4.0, 'f': 4.0},
        {'type': 'pop',  'state': (0, 0), 'g': 0,
         'h': 4.0, 'f': 4.0},
        {'type': 'push', 'state': (0, 1), 'g': 1,
         'parent': (0, 0), 'h': 3.0, 'f': 4.0},
        {'type': 'push', 'state': (1, 0), 'g': 1,
         'parent': (0, 0), 'h': 3.0, 'f': 4.0},
        {'type': 'pop',  'state': (0, 1), 'g': 1,
         'h': 3.0, 'f': 4.0},
        {'type': 'push', 'state': (0, 2), 'g': 2,
         'parent': (0, 1), 'h': 2.0, 'f': 4.0},
        {'type': 'push', 'state': (1, 1), 'g': 2,
         'parent': (0, 1), 'h': 2.0, 'f': 4.0},
        {'type': 'pop',  'state': (0, 2), 'g': 2,
         'h': 2.0, 'f': 4.0},
        {'type': 'push', 'state': (1, 2), 'g': 3,
         'parent': (0, 2), 'h': 1.0, 'f': 4.0},
        {'type': 'pop',  'state': (1, 2), 'g': 3,
         'h': 1.0, 'f': 4.0},
        {'type': 'push', 'state': (2, 2), 'g': 4,
         'parent': (1, 2), 'h': 0.0, 'f': 4.0},
        {'type': 'pop',  'state': (2, 2), 'g': 4,
         'h': 0.0, 'f': 4.0},
    ]
    assert actual == expected
    # Every event has f = g + h.
    for e in actual:
        assert e['f'] == e['g'] + e['h']


def test_recording_full_event_sequence_on_grid_3x3_obstacle() -> None:
    """
    ========================================================================
     Assert the exact recorded event sequence for AStar on a 3x3
     grid with obstacle at (1,1), from (0,0) to (2,2), Manhattan h.
     Obstacle cell (1,1) never appears as state or parent in any
     event. The search still finds cost 4 (going around the
     obstacle via the top-right or bottom-left corridor).
    ========================================================================
    """
    problem = ProblemGrid.Factory.grid_3x3_obstacle()
    goal = problem.goal
    algo = AStar(problem=problem,
                 h=lambda s: float(s.distance(goal)),
                 is_recording=True)
    algo.run()
    actual = [_normalize(e) for e in algo.recorder.events]
    expected = [
        {'type': 'push', 'state': (0, 0), 'g': 0,
         'parent': None, 'h': 4.0, 'f': 4.0},
        {'type': 'pop',  'state': (0, 0), 'g': 0,
         'h': 4.0, 'f': 4.0},
        {'type': 'push', 'state': (0, 1), 'g': 1,
         'parent': (0, 0), 'h': 3.0, 'f': 4.0},
        {'type': 'push', 'state': (1, 0), 'g': 1,
         'parent': (0, 0), 'h': 3.0, 'f': 4.0},
        {'type': 'pop',  'state': (0, 1), 'g': 1,
         'h': 3.0, 'f': 4.0},
        {'type': 'push', 'state': (0, 2), 'g': 2,
         'parent': (0, 1), 'h': 2.0, 'f': 4.0},
        {'type': 'pop',  'state': (0, 2), 'g': 2,
         'h': 2.0, 'f': 4.0},
        {'type': 'push', 'state': (1, 2), 'g': 3,
         'parent': (0, 2), 'h': 1.0, 'f': 4.0},
        {'type': 'pop',  'state': (1, 2), 'g': 3,
         'h': 1.0, 'f': 4.0},
        {'type': 'push', 'state': (2, 2), 'g': 4,
         'parent': (1, 2), 'h': 0.0, 'f': 4.0},
        {'type': 'pop',  'state': (2, 2), 'g': 4,
         'h': 0.0, 'f': 4.0},
    ]
    assert actual == expected
    # Obstacle cell (1,1) never appears as state or parent.
    obstacle = (1, 1)
    for e in actual:
        assert e['state'] != obstacle
        if 'parent' in e and e['parent'] is not None:
            assert e['parent'] != obstacle


def test_recording_full_event_sequence_on_grid_4x4_obstacle() -> None:
    """
    ========================================================================
     Assert the exact recorded event sequence for AStar on a 4x4
     grid with a vertical 2-cell wall at (0,2) and (1,2).
     Start (0,0) -> Goal (0,3). The wall forces a 7-step detour
     through row 2. Manhattan h is admissible but loose (ignores
     the wall) — f-values along the detour rise to 5, 7, 9 as
     A* expands into row 1, 2, 3 before reaching the goal.
     Obstacle cells (0,2) and (1,2) never appear as state or
     parent in any event. 11 pushes + 11 pops — vs. BFS's 14+14
     on the same problem, showing the heuristic's pruning power.
    ========================================================================
    """
    problem = ProblemGrid.Factory.grid_4x4_obstacle()
    goal = problem.goal
    algo = AStar(problem=problem,
                 h=lambda s: float(s.distance(goal)),
                 is_recording=True)
    algo.run()
    actual = [_normalize(e) for e in algo.recorder.events]
    expected = [
        {'type': 'push', 'state': (0, 0), 'g': 0, 'parent': None, 'h': 3.0, 'f': 3.0},
        {'type': 'pop',  'state': (0, 0), 'g': 0, 'h': 3.0, 'f': 3.0},
        {'type': 'push', 'state': (0, 1), 'g': 1, 'parent': (0, 0), 'h': 2.0, 'f': 3.0},
        {'type': 'push', 'state': (1, 0), 'g': 1, 'parent': (0, 0), 'h': 4.0, 'f': 5.0},
        {'type': 'pop',  'state': (0, 1), 'g': 1, 'h': 2.0, 'f': 3.0},
        {'type': 'push', 'state': (1, 1), 'g': 2, 'parent': (0, 1), 'h': 3.0, 'f': 5.0},
        {'type': 'pop',  'state': (1, 1), 'g': 2, 'h': 3.0, 'f': 5.0},
        {'type': 'push', 'state': (2, 1), 'g': 3, 'parent': (1, 1), 'h': 4.0, 'f': 7.0},
        {'type': 'pop',  'state': (1, 0), 'g': 1, 'h': 4.0, 'f': 5.0},
        {'type': 'push', 'state': (2, 0), 'g': 2, 'parent': (1, 0), 'h': 5.0, 'f': 7.0},
        {'type': 'pop',  'state': (2, 1), 'g': 3, 'h': 4.0, 'f': 7.0},
        {'type': 'push', 'state': (2, 2), 'g': 4, 'parent': (2, 1), 'h': 3.0, 'f': 7.0},
        {'type': 'push', 'state': (3, 1), 'g': 4, 'parent': (2, 1), 'h': 5.0, 'f': 9.0},
        {'type': 'pop',  'state': (2, 2), 'g': 4, 'h': 3.0, 'f': 7.0},
        {'type': 'push', 'state': (2, 3), 'g': 5, 'parent': (2, 2), 'h': 2.0, 'f': 7.0},
        {'type': 'push', 'state': (3, 2), 'g': 5, 'parent': (2, 2), 'h': 4.0, 'f': 9.0},
        {'type': 'pop',  'state': (2, 3), 'g': 5, 'h': 2.0, 'f': 7.0},
        {'type': 'push', 'state': (1, 3), 'g': 6, 'parent': (2, 3), 'h': 1.0, 'f': 7.0},
        {'type': 'push', 'state': (3, 3), 'g': 6, 'parent': (2, 3), 'h': 3.0, 'f': 9.0},
        {'type': 'pop',  'state': (1, 3), 'g': 6, 'h': 1.0, 'f': 7.0},
        {'type': 'push', 'state': (0, 3), 'g': 7, 'parent': (1, 3), 'h': 0.0, 'f': 7.0},
        {'type': 'pop',  'state': (0, 3), 'g': 7, 'h': 0.0, 'f': 7.0},
    ]
    assert actual == expected
    # Obstacle cells never appear as state or parent.
    obstacles = {(0, 2), (1, 2)}
    for e in actual:
        assert e['state'] not in obstacles
        if 'parent' in e and e['parent'] is not None:
            assert e['parent'] not in obstacles


def test_recording_is_cached_marker_on_graph_abc_cached_at_b() -> None:
    """
    ========================================================================
     With HCached covering {B, C}, AStar pops A (not cached,
     so no marker), expands to B, pops B and early-exits.
     Recorded sequence:
       push(A), pop(A),
       push(B, is_cached=True), pop(B, is_cached=True).

     Pins:
       1. `is_cached=True` appears on push AND pop of cached
          states; absent (not False) on uncached events —
          framework Recording Principle forbids constant-False
          flags.
       2. No dedicated `cache_hit` event — the terminator is
          readable as "last pop carrying is_cached=True",
          mirroring goal-pop-is-implicit.
       3. `search_state.cache_hit` state field still set — only
          the event was dropped.
    ========================================================================
    """
    algo = AStar.Factory.graph_abc_cached_at_b()
    algo._recorder.is_active = True
    sol = algo.run()
    assert sol.cost == 2.0

    actual = [_normalize(e) for e in algo.recorder.events]
    expected = [
        {'type': 'push', 'state': 'A', 'g': 0, 'parent': None, 'h': 2.0, 'f': 2.0},
        {'type': 'pop',  'state': 'A', 'g': 0, 'h': 2.0, 'f': 2.0},
        {'type': 'push', 'state': 'B', 'g': 1, 'parent': 'A', 'h': 1.0, 'f': 2.0, 'is_cached': True},
        {'type': 'pop',  'state': 'B', 'g': 1, 'h': 1.0, 'f': 2.0, 'is_cached': True},
    ]
    assert actual == expected

    # Cache-hit pops uniquely marked — the terminator is
    # identifiable without a dedicated event type.
    cached_pops = [e for e in actual
                   if e['type'] == 'pop' and e.get('is_cached')]
    assert len(cached_pops) == 1
    assert cached_pops[0]['state'] == 'B'
    # `is_cached` absent (not False) on uncached events.
    for e in actual:
        if e['state'] != 'B':
            assert 'is_cached' not in e
    # search_state.cache_hit state field still set.
    assert algo.search_state.cache_hit is not None
    assert algo.search_state.cache_hit.key == 'B'


def test_recording_on_grid_4x4_obstacle_with_cached_optimal_suffix() -> None:
    """
    ========================================================================
     AStar on grid_4x4_obstacle (wall at (0,2), (1,2);
     (0,0) -> (0,3)) with an HCached covering the optimal path
     from (0,1) to (0,3). The start (0,0) is NOT cached, so
     the search must take one real expansion step before it
     can benefit from the cache.

     Cache contents (7 states, tight h* and suffix_next):

       (0,1) h*=6 next=(1,1)   (2,2) h*=3 next=(2,3)
       (1,1) h*=5 next=(2,1)   (2,3) h*=2 next=(1,3)
       (2,1) h*=4 next=(2,2)   (1,3) h*=1 next=(0,3)
                               (0,3) h*=0 next=None

     The base Manhattan heuristic is admissible-but-loose
     (ignores the wall). On cached states it's dominated by the
     tighter cached h* (e.g., h*((0,1))=6 vs Manhattan=2). So
     AStar's (f,-g) comparison prefers the uncached neighbor
     (1,0) over the cached (0,1) — the cache does NOT merely
     bait the search into cached states; optimality is preserved
     because cached f-values remain tight bounds on actual cost.

     Event sequence — 8 events vs 22 for the un-cached run
     (see `test_recording_full_event_sequence_on_grid_4x4_obstacle`):

       1. push (0,0) f=3
       2. pop  (0,0)
       3. push (0,1) f=7 is_cached=True
       4. push (1,0) f=5
       5. pop  (1,0)                    # (1,0) f=5 < (0,1) f=7
       6. push (1,1) f=7 is_cached=True
       7. push (2,0) f=7
       8. pop  (1,1) is_cached=True     # early-exit cost 2+5=7

     Pins, beyond the previous cache test:
       a. `is_cached=True` shows up BEFORE the terminating pop
          (on pushes of (0,1) and (1,1)), giving consumers
          visibility into the cache's role throughout the search.
       b. A cached state can be pushed but never popped — (0,1)
          is dominated by (1,0)'s lower f and pops out. This
          distinguishes "touched by cache" (push-visibility)
          from "terminated via cache" (last-pop-is_cached).
       c. Tie-break at f=7 across three states ((0,1), (1,1),
          (2,0)) — (-g, state) picks (1,1) deterministically.
       d. Optimal cost 7 matches the un-cached run, i.e., the
          cache didn't break admissibility.
       e. reconstruct_path stitches the walked parent chain
          (0,0)->(1,0)->(1,1) with the cached suffix
          (2,1)->(2,2)->(2,3)->(1,3)->(0,3) into the full
          8-state optimal path.
    ========================================================================
    """
    problem = ProblemGrid.Factory.grid_4x4_obstacle()
    goal = problem.goal   # StateCell at (0, 3)

    # Externally-built StateCell instances; equality via HasKey
    # (CellMap) matches the problem's internal cache by key.
    def sc(r: int, c: int) -> StateCell:
        return StateCell(key=CellMap(row=r, col=c))

    p01, p11, p21, p22 = sc(0, 1), sc(1, 1), sc(2, 1), sc(2, 2)
    p23, p13, p03      = sc(2, 3), sc(1, 3), sc(0, 3)

    cache = {
        p01: CacheEntry(h_perfect=6.0, suffix_next=p11),
        p11: CacheEntry(h_perfect=5.0, suffix_next=p21),
        p21: CacheEntry(h_perfect=4.0, suffix_next=p22),
        p22: CacheEntry(h_perfect=3.0, suffix_next=p23),
        p23: CacheEntry(h_perfect=2.0, suffix_next=p13),
        p13: CacheEntry(h_perfect=1.0, suffix_next=p03),
        p03: CacheEntry(h_perfect=0.0, suffix_next=None),
    }
    h = HCached(
        base=HCallable(fn=lambda s: float(s.distance(goal))),
        cache=cache,
        goal=p03,   # == problem.goal via HasKey
    )
    algo = AStar(problem=problem, h=h, is_recording=True)

    sol = algo.run()
    assert sol.cost == 7.0

    actual = [_normalize(e) for e in algo.recorder.events]
    expected = [
        {'type': 'push', 'state': (0, 0), 'g': 0, 'parent': None, 'h': 3.0, 'f': 3.0},
        {'type': 'pop',  'state': (0, 0), 'g': 0, 'h': 3.0, 'f': 3.0},
        {'type': 'push', 'state': (0, 1), 'g': 1, 'parent': (0, 0), 'h': 6.0, 'f': 7.0, 'is_cached': True},
        {'type': 'push', 'state': (1, 0), 'g': 1, 'parent': (0, 0), 'h': 4.0, 'f': 5.0},
        {'type': 'pop',  'state': (1, 0), 'g': 1, 'h': 4.0, 'f': 5.0},
        {'type': 'push', 'state': (1, 1), 'g': 2, 'parent': (1, 0), 'h': 5.0, 'f': 7.0, 'is_cached': True},
        {'type': 'push', 'state': (2, 0), 'g': 2, 'parent': (1, 0), 'h': 5.0, 'f': 7.0},
        {'type': 'pop',  'state': (1, 1), 'g': 2, 'h': 5.0, 'f': 7.0, 'is_cached': True},
    ]
    assert actual == expected
    assert len(actual) == 8   # 8 events vs 22 un-cached

    # is_cached markers — visible on cache interactions
    # throughout the search, not only at termination.
    cached_pushes = [e for e in actual
                     if e['type'] == 'push' and e.get('is_cached')]
    cached_pops = [e for e in actual
                   if e['type'] == 'pop' and e.get('is_cached')]
    assert {e['state'] for e in cached_pushes} == {(0, 1), (1, 1)}
    assert len(cached_pops) == 1
    assert cached_pops[0]['state'] == (1, 1)

    # (0,1) is pushed (cached) but never popped — dominated by
    # (1,0)'s lower f. Distinguishes visibility from termination.
    popped_states = {e['state'] for e in actual
                     if e['type'] == 'pop'}
    assert (0, 1) not in popped_states

    # is_cached absent (not False) on uncached events.
    for e in actual:
        if e['state'] not in {(0, 1), (1, 1)}:
            assert 'is_cached' not in e

    # Terminator is readable from the log: last pop's is_cached.
    assert actual[-1]['type'] == 'pop'
    assert actual[-1].get('is_cached') is True

    # search_state.cache_hit state field
    assert algo.search_state.cache_hit is not None
    assert algo.search_state.cache_hit.rc == (1, 1)
    assert algo.search_state.goal_reached is None

    # reconstruct_path stitches prefix + cached suffix.
    path = algo.reconstruct_path()
    assert [s.rc for s in path] == [
        (0, 0), (1, 0), (1, 1),                         # prefix
        (2, 1), (2, 2), (2, 3), (1, 3), (0, 3),         # suffix
    ]


def test_recording_resume_from_seeded_search_state() -> None:
    """
    ========================================================================
     Inject a pre-built SearchStateSPP into AStar and pump with
     resume(). Seed: on graph_abc (A -> B -> C), pretend A has
     already been popped-and-closed and B is sitting on the
     frontier with g=1, parent=A. resume() records only the
     post-seed events:
         pop(B), push(C), pop(C)
     — no A events, confirming that the seeded bundle persists
     through the resume() entry point (no _init_search clears
     it). Pins two things at once:
       1. The new `search_state` kwarg on AStar.__init__ wires
          through to AlgoSPP and replaces the fresh bundle.
       2. `_goals_set` is populated at init time (not only in
          _init_search), so `_is_goal(C)` fires correctly on
          the first pop under a resume-only code path.
    ========================================================================
    """
    problem = ProblemSPP.Factory.graph_abc()
    a = StateBase[str](key='A')
    b = StateBase[str](key='B')

    # Pre-built bundle: A closed, B's g/parent set. Frontier is
    # constructed empty — we push B after the AStar instance is
    # available (priority depends on the h stored on AStar).
    seed = SearchStateSPP[StateBase[str]](
        frontier=FrontierPriority[StateBase[str]](),
        g={a: 0.0, b: 1.0},
        parent={a: None, b: a},
        closed={a},
    )
    h_map = {'A': 2.0, 'B': 1.0, 'C': 0.0}
    algo = AStar(
        problem=problem,
        h=lambda s: h_map.get(s.key, 0.0),
        is_recording=True,
        search_state=seed,
    )
    # Push B via the low-level frontier API so the seed doesn't
    # pollute the recorder — we want the log to contain ONLY
    # post-resume events.
    seed.frontier.push(state=b, priority=algo._priority(state=b))

    sol = algo.resume()
    assert sol.cost == 2.0

    actual = [_normalize(e) for e in algo.recorder.events]
    expected = [
        {'type': 'pop',  'state': 'B', 'g': 1, 'h': 1.0, 'f': 2.0},
        {'type': 'push', 'state': 'C', 'g': 2, 'parent': 'B', 'h': 0.0, 'f': 2.0},
        {'type': 'pop',  'state': 'C', 'g': 2, 'h': 0.0, 'f': 2.0},
    ]
    assert actual == expected
    # A never appears as state or parent in the post-resume log.
    for e in actual:
        assert e['state'] != 'A'
        if 'parent' in e:
            assert e['parent'] != 'A'
    # search_state identity — the injected bundle is the one
    # AStar mutated.
    assert algo.search_state is seed
    assert seed.goal_reached is not None
    assert seed.goal_reached.key == 'C'


def test_recording_grid_4x4_reuse_state_from_prior_goal_2_1() -> None:
    """
    ========================================================================
     Two-stage AStar on a 4x4 grid with wall at (0,2), (1,2):

       Stage 1: solve (0,0) -> (2,1) under Manhattan h. Discard
                the events (not recorded); keep the final
                SearchStateSPP.
       Stage 2: inject that SearchStateSPP into a fresh AStar on
                the SAME grid with goal (0,3), under the new
                Manhattan h. resume(); record every event from
                the resume-point onward.

     The prior-search bundle carries:
       closed       = {(0,0), (0,1), (1,1)}
       g / parent   entries for (0,0), (0,1), (1,0), (1,1), (2,1)
       frontier     = [(1,0)] with STALE priority f=3 (computed
                       against the OLD goal (2,1))
       goal_reached = (2,1)          — old goal

     AStar's auto-refresh (dirty flag set at __init__ because a
     search_state was supplied) recomputes (1,0)'s priority for
     the NEW goal (0,3) — f becomes 1+4=5 (Manhattan to (0,3)).
     The refresh emits NO events (it's setup, not a search step).

     Post-resume event sequence (17 events):

       pop  (1,0)    f=5
       push (2,0)                 f=7
       pop  (2,0)                 f=7
       push (2,1)  parent=(2,0)   f=7     # re-parented from (1,1)
       push (3,0)                 f=9
       pop  (2,1)                 f=7
       push (2,2)                 f=7
       push (3,1)                 f=9
       pop  (2,2)                 f=7
       push (2,3)                 f=7
       push (3,2)                 f=9
       pop  (2,3)                 f=7
       push (3,3)                 f=9
       push (1,3)                 f=7
       pop  (1,3)                 f=7
       push (0,3)                 f=7
       pop  (0,3)                 f=7     # NEW goal -> cost 7

     Pins, in addition to the exact event sequence:
       1. Dirty flag True at __init__, False after resume.
       2. `goal_reached` is OVERWRITTEN from (2,1) to (0,3).
       3. (2,1) — the OLD goal and never-closed in the seed —
          is now reached via (2,0) in the new search and gets
          its parent rewritten. Same g=3 (coincidentally both
          paths are optimal) so no consistency breakage.
       4. The old goal (2,1) is NOT a goal in the new problem
          and is legitimately expanded.
       5. Reuse is NOT always a win: first search (9 events) +
          second (17 events) = 26 total, which is MORE than
          from-scratch (22 events for grid_4x4_obstacle). The
          prior exploration didn't overlap enough with the new
          search's needs. The test is a CORRECTNESS pin, not a
          performance pin.
    ========================================================================
    """
    # ---- Stage 1: prior AStar with goal (2,1) --------------------
    grid = GridMap(rows=4)
    grid[0][2].set_invalid()
    grid[1][2].set_invalid()
    problem_first = ProblemGrid(
        grid=grid,
        start=grid[0][0],
        goal=grid[2][1],
    )
    goal_first = problem_first.goal
    algo_first = AStar(
        problem=problem_first,
        h=lambda s: float(s.distance(goal_first)),
    )
    sol_first = algo_first.run()
    assert sol_first.cost == 3.0
    assert algo_first.search_state.goal_reached.rc == (2, 1)

    # ---- Stage 2: new AStar goal (0,3); inject prior state ------
    problem_second = ProblemGrid.Factory.grid_4x4_obstacle()
    goal_second = problem_second.goal   # (0, 3)
    algo_second = AStar(
        problem=problem_second,
        h=lambda s: float(s.distance(goal_second)),
        is_recording=True,
        search_state=algo_first.search_state,
    )
    assert algo_second._frontier_dirty is True
    # The seed's old goal is still sitting on goal_reached.
    assert algo_second.search_state.goal_reached.rc == (2, 1)

    sol = algo_second.resume()
    assert sol.cost == 7.0
    # Dirty flag cleared after the one-shot refresh.
    assert algo_second._frontier_dirty is False
    # The NEW goal overwrites the seed's.
    assert algo_second.search_state.goal_reached is not None
    assert algo_second.search_state.goal_reached.rc == (0, 3)

    actual = [_normalize(e) for e in algo_second.recorder.events]
    expected = [
        {'type': 'pop',  'state': (1, 0), 'g': 1, 'h': 4.0, 'f': 5.0},
        {'type': 'push', 'state': (2, 0), 'g': 2, 'parent': (1, 0), 'h': 5.0, 'f': 7.0},
        {'type': 'pop',  'state': (2, 0), 'g': 2, 'h': 5.0, 'f': 7.0},
        {'type': 'push', 'state': (2, 1), 'g': 3, 'parent': (2, 0), 'h': 4.0, 'f': 7.0},
        {'type': 'push', 'state': (3, 0), 'g': 3, 'parent': (2, 0), 'h': 6.0, 'f': 9.0},
        {'type': 'pop',  'state': (2, 1), 'g': 3, 'h': 4.0, 'f': 7.0},
        {'type': 'push', 'state': (2, 2), 'g': 4, 'parent': (2, 1), 'h': 3.0, 'f': 7.0},
        {'type': 'push', 'state': (3, 1), 'g': 4, 'parent': (2, 1), 'h': 5.0, 'f': 9.0},
        {'type': 'pop',  'state': (2, 2), 'g': 4, 'h': 3.0, 'f': 7.0},
        {'type': 'push', 'state': (2, 3), 'g': 5, 'parent': (2, 2), 'h': 2.0, 'f': 7.0},
        {'type': 'push', 'state': (3, 2), 'g': 5, 'parent': (2, 2), 'h': 4.0, 'f': 9.0},
        {'type': 'pop',  'state': (2, 3), 'g': 5, 'h': 2.0, 'f': 7.0},
        {'type': 'push', 'state': (1, 3), 'g': 6, 'parent': (2, 3), 'h': 1.0, 'f': 7.0},
        {'type': 'push', 'state': (3, 3), 'g': 6, 'parent': (2, 3), 'h': 3.0, 'f': 9.0},
        {'type': 'pop',  'state': (1, 3), 'g': 6, 'h': 1.0, 'f': 7.0},
        {'type': 'push', 'state': (0, 3), 'g': 7, 'parent': (1, 3), 'h': 0.0, 'f': 7.0},
        {'type': 'pop',  'state': (0, 3), 'g': 7, 'h': 0.0, 'f': 7.0},
    ]
    assert actual == expected
    assert len(actual) == 17

    # No is_cached markers (no HCached used).
    for e in actual:
        assert 'is_cached' not in e

    # (2,1) — old goal — re-parented from (1,1) in the seed to
    # (2,0) after the second search's expansion. Same g=3.
    parent_21 = algo_second.search_state.parent[
        StateCell(key=CellMap(row=2, col=1))]
    assert parent_21.rc == (2, 0)
    assert algo_second.search_state.g[
        StateCell(key=CellMap(row=2, col=1))] == 3.0


def test_recording_hbounded_tightens_h_on_grid_4x4_obstacle() -> None:
    """
    ========================================================================
     AStar on grid_4x4_obstacle with Manhattan wrapped in an
     HBounded that bounds (1,0) at h=6 (tight — h*((1,0))=6).
     Un-bounded Manhattan gives h((1,0))=4, f=5 — (1,0) pops
     right after (0,1). Bounded gives h=6, f=7 — (1,0) is
     dominated by (2,1) f=7 -g=-3 and never pops, eliminating
     (1,0)'s expansion entirely.

     Effect vs. un-bounded 22-event sequence:
       - (1,0) push carries h=6.0, f=7.0 (not h=4, f=5).
       - (1,0) never appears in a pop event.
       - (2,0) is pushed from (2,1) at g=4 (not from (1,0) at g=2).
       - Total: 13 pushes + 8 pops = 21 events (vs. 22).

     Pins:
       a. HBounded routes through AStar._priority unchanged —
          zero AStar edits needed.
       b. is_cached never appears (HBounded.is_perfect = False
          always, so cache_rank stays 1).
       c. Optimal cost 7 preserved (admissibility held).
    ========================================================================
    """
    def sc(r: int, c: int) -> StateCell:
        return StateCell(key=CellMap(row=r, col=c))

    problem = ProblemGrid.Factory.grid_4x4_obstacle()
    goal = problem.goal
    bounds = {sc(1, 0): 6.0}
    h = HBounded(
        base=HCallable(fn=lambda s: float(s.distance(goal))),
        bounds=bounds,
    )
    algo = AStar(problem=problem, h=h, is_recording=True)
    sol = algo.run()
    assert sol.cost == 7.0

    actual = [_normalize(e) for e in algo.recorder.events]
    expected = [
        {'type': 'push', 'state': (0, 0), 'g': 0, 'parent': None, 'h': 3.0, 'f': 3.0},
        {'type': 'pop',  'state': (0, 0), 'g': 0, 'h': 3.0, 'f': 3.0},
        {'type': 'push', 'state': (0, 1), 'g': 1, 'parent': (0, 0), 'h': 2.0, 'f': 3.0},
        {'type': 'push', 'state': (1, 0), 'g': 1, 'parent': (0, 0), 'h': 6.0, 'f': 7.0, 'is_bounded': True},
        {'type': 'pop',  'state': (0, 1), 'g': 1, 'h': 2.0, 'f': 3.0},
        {'type': 'push', 'state': (1, 1), 'g': 2, 'parent': (0, 1), 'h': 3.0, 'f': 5.0},
        {'type': 'pop',  'state': (1, 1), 'g': 2, 'h': 3.0, 'f': 5.0},
        {'type': 'push', 'state': (2, 1), 'g': 3, 'parent': (1, 1), 'h': 4.0, 'f': 7.0},
        {'type': 'pop',  'state': (2, 1), 'g': 3, 'h': 4.0, 'f': 7.0},
        {'type': 'push', 'state': (2, 2), 'g': 4, 'parent': (2, 1), 'h': 3.0, 'f': 7.0},
        {'type': 'push', 'state': (3, 1), 'g': 4, 'parent': (2, 1), 'h': 5.0, 'f': 9.0},
        {'type': 'push', 'state': (2, 0), 'g': 4, 'parent': (2, 1), 'h': 5.0, 'f': 9.0},
        {'type': 'pop',  'state': (2, 2), 'g': 4, 'h': 3.0, 'f': 7.0},
        {'type': 'push', 'state': (2, 3), 'g': 5, 'parent': (2, 2), 'h': 2.0, 'f': 7.0},
        {'type': 'push', 'state': (3, 2), 'g': 5, 'parent': (2, 2), 'h': 4.0, 'f': 9.0},
        {'type': 'pop',  'state': (2, 3), 'g': 5, 'h': 2.0, 'f': 7.0},
        {'type': 'push', 'state': (1, 3), 'g': 6, 'parent': (2, 3), 'h': 1.0, 'f': 7.0},
        {'type': 'push', 'state': (3, 3), 'g': 6, 'parent': (2, 3), 'h': 3.0, 'f': 9.0},
        {'type': 'pop',  'state': (1, 3), 'g': 6, 'h': 1.0, 'f': 7.0},
        {'type': 'push', 'state': (0, 3), 'g': 7, 'parent': (1, 3), 'h': 0.0, 'f': 7.0},
        {'type': 'pop',  'state': (0, 3), 'g': 7, 'h': 0.0, 'f': 7.0},
    ]
    assert actual == expected
    assert len(actual) == 21

    # (1,0) pushed at h=6 (tight) but never popped — dominated.
    popped_states = {e['state'] for e in actual
                     if e['type'] == 'pop'}
    assert (1, 0) not in popped_states
    push_10 = [e for e in actual
               if e['type'] == 'push' and e['state'] == (1, 0)][0]
    assert push_10['h'] == 6.0 and push_10['f'] == 7.0
    # is_bounded=True on the bounded push (strict: 6 > Manhattan 4).
    assert push_10.get('is_bounded') is True

    # is_bounded appears only on the (1,0) push — no other state
    # is in the bounds dict; all others absent (not False).
    for e in actual:
        if e['state'] != (1, 0):
            assert 'is_bounded' not in e

    # No is_cached anywhere (HBounded.is_perfect is False).
    for e in actual:
        assert 'is_cached' not in e


def test_recording_hbounded_after_pathmax_propagation_depth_2() -> None:
    """
    ========================================================================
     AStar on grid_4x4_obstacle with HBounded seeded at (1,1)=5.
     Call propagate_pathmax(depth=2) BEFORE run(). Verifies the
     propagated bound (0,1)=4 manifests in recorded events.

     Pathmax trace:
       Wave 1: seed={(1,1)}. Successors (0,1), (2,1), (1,0).
         - (0,1): Manhattan=2, cand=5-1=4 > 2 → bound (0,1)=4.
         - (2,1): Manhattan=4, cand=4 ≤ 4 → no.
         - (1,0): Manhattan=4, cand=4 ≤ 4 → no.
       Wave 2: source={(0,1)}. Successors (1,1), (0,0).
         - (1,1): h=5, cand=4-1=3 ≤ 5 → no.
         - (0,0): Manhattan=3, cand=3 ≤ 3 → no.
       Final bounds: {(1,1): 5.0, (0,1): 4.0}.
       Returned updates: {(0,1): 4.0}.

     Search: 22 events (same reordering regime as single-bound
     sibling test, plus (0,1) now also carries the marker).
     `is_bounded=True` on push AND pop of BOTH (0,1) AND (1,1).

     Pins:
       1. propagate_pathmax actually mutates HBounded's bounds.
       2. Propagated bound (0,1)=4 manifests in recorded h/f.
       3. is_bounded=True on push AND pop of BOTH propagated
          (0,1) AND seeded (1,1) — one search exercises both
          sources of is_bounded markers.
       4. Admissibility preserved — optimal cost 7.
       5. Returned dict is the tightened subset ({(0,1): 4.0}),
          NOT the seeds.
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
    algo = AStar(problem=problem, h=h, is_recording=True)

    updates = algo.propagate_pathmax(depth=2)
    assert updates == {sc(0, 1): 4.0}
    assert h(sc(0, 1)) == 4.0
    assert h(sc(1, 1)) == 5.0

    sol = algo.run()
    assert sol.cost == 7.0

    actual = [_normalize(e) for e in algo.recorder.events]
    expected = [
        # Propagate event — wave 1 from seed (1,1)=5 tightens
        # (0,1) from Manhattan 2 to 4. Wave 2 is degenerate.
        {'type': 'propagate', 'state': (0, 1),
         'parent': (1, 1), 'h_parent': 5.0, 'h': 4.0},
        # Search events (22).
        {'type': 'push', 'state': (0, 0), 'g': 0, 'parent': None,
         'h': 3.0, 'f': 3.0},
        {'type': 'pop',  'state': (0, 0), 'g': 0,
         'h': 3.0, 'f': 3.0},
        {'type': 'push', 'state': (0, 1), 'g': 1, 'parent': (0, 0),
         'h': 4.0, 'f': 5.0, 'is_bounded': True},
        {'type': 'push', 'state': (1, 0), 'g': 1, 'parent': (0, 0),
         'h': 4.0, 'f': 5.0},
        {'type': 'pop',  'state': (0, 1), 'g': 1,
         'h': 4.0, 'f': 5.0, 'is_bounded': True},
        {'type': 'push', 'state': (1, 1), 'g': 2, 'parent': (0, 1),
         'h': 5.0, 'f': 7.0, 'is_bounded': True},
        {'type': 'pop',  'state': (1, 0), 'g': 1,
         'h': 4.0, 'f': 5.0},
        {'type': 'push', 'state': (2, 0), 'g': 2, 'parent': (1, 0),
         'h': 5.0, 'f': 7.0},
        {'type': 'pop',  'state': (1, 1), 'g': 2,
         'h': 5.0, 'f': 7.0, 'is_bounded': True},
        {'type': 'push', 'state': (2, 1), 'g': 3, 'parent': (1, 1),
         'h': 4.0, 'f': 7.0},
        {'type': 'pop',  'state': (2, 1), 'g': 3,
         'h': 4.0, 'f': 7.0},
        {'type': 'push', 'state': (2, 2), 'g': 4, 'parent': (2, 1),
         'h': 3.0, 'f': 7.0},
        {'type': 'push', 'state': (3, 1), 'g': 4, 'parent': (2, 1),
         'h': 5.0, 'f': 9.0},
        {'type': 'pop',  'state': (2, 2), 'g': 4,
         'h': 3.0, 'f': 7.0},
        {'type': 'push', 'state': (2, 3), 'g': 5, 'parent': (2, 2),
         'h': 2.0, 'f': 7.0},
        {'type': 'push', 'state': (3, 2), 'g': 5, 'parent': (2, 2),
         'h': 4.0, 'f': 9.0},
        {'type': 'pop',  'state': (2, 3), 'g': 5,
         'h': 2.0, 'f': 7.0},
        {'type': 'push', 'state': (1, 3), 'g': 6, 'parent': (2, 3),
         'h': 1.0, 'f': 7.0},
        {'type': 'push', 'state': (3, 3), 'g': 6, 'parent': (2, 3),
         'h': 3.0, 'f': 9.0},
        {'type': 'pop',  'state': (1, 3), 'g': 6,
         'h': 1.0, 'f': 7.0},
        {'type': 'push', 'state': (0, 3), 'g': 7, 'parent': (1, 3),
         'h': 0.0, 'f': 7.0},
        {'type': 'pop',  'state': (0, 3), 'g': 7,
         'h': 0.0, 'f': 7.0},
    ]
    assert actual == expected
    assert len(actual) == 23  # 1 propagate + 22 search

    # Propagate event schema pins.
    propagate_events = [e for e in actual
                        if e['type'] == 'propagate']
    assert len(propagate_events) == 1
    p = propagate_events[0]
    assert p == {'type': 'propagate', 'state': (0, 1),
                 'parent': (1, 1), 'h_parent': 5.0, 'h': 4.0}
    # No g/f on propagate events (pre-search; not applicable).
    assert 'g' not in p
    assert 'f' not in p

    # is_bounded on push AND pop of BOTH (0,1) and (1,1).
    bounded = [e for e in actual if e.get('is_bounded')]
    assert len(bounded) == 4
    by_state: dict[tuple, set[str]] = {}
    for e in bounded:
        by_state.setdefault(e['state'], set()).add(e['type'])
    assert by_state == {(0, 1): {'push', 'pop'},
                        (1, 1): {'push', 'pop'}}

    # is_bounded absent from every other event.
    for e in actual:
        if e['state'] not in {(0, 1), (1, 1)}:
            assert 'is_bounded' not in e

    # No is_cached anywhere.
    for e in actual:
        assert 'is_cached' not in e


def test_recording_pathmax_multiwave_from_start_seed_prunes_on_grid_4x4() -> None:
    """
    ========================================================================
     AStar on grid_4x4_obstacle with HBounded seeded at **(0,0)=7**
     — the start state itself, tight (h*((0,0))=7). Call
     `propagate_pathmax(depth=2)` BEFORE run().

     Pathmax trace:
       Wave 1: source={(0,0)}. Successors (0,1), (1,0).
         - (0,1): Manhattan=2, cand=7-1=6 > 2 → bound (0,1)=6.
         - (1,0): Manhattan=4, cand=7-1=6 > 4 → bound (1,0)=6.
       Wave 2: source={(0,1), (1,0)}.
         - From (0,1)=6: candidates to (1,1) [Manhattan=3,
           cand=5 > 3 → bound (1,1)=5] and to (0,0) [h=7, no].
         - From (1,0)=6: candidates to (0,0) [h=7, no], (1,1)
           [h=5 after first tightening OR Manhattan=3 if
           processed first; cand=5 ties existing 5 OR beats
           Manhattan 3 — depends on set order, but either way
           (1,1) ends at 5; add_bound is idempotent on second
           attempt], (2,0) [Manhattan=5, cand=5 tie, no].

       Final bounds: {(0,0):7, (0,1):6, (1,0):6, (1,1):5}.
       Returned updates = {(0,1):6, (1,0):6, (1,1):5} (seeds
       not included).

     Search effect — 21 events (vs. 22 un-propagated):
       - (1,0) is pushed with is_bounded=True but NEVER popped;
         dominated by every f=7 state with -g < -1. This is
         pathmax-driven PRUNING, not mere reordering.
       - is_bounded markers on 7 events: push+pop of (0,0),
         (0,1), (1,1) [6] PLUS push-only of (1,0) [1] — the
         push-only case proves the flag fires on pruned pushes
         too, not only on popped states.
       - Optimal cost 7 preserved.

     Pins not covered by the depth-2 predecessor test:
       1. A wave-2 update actually happens ((1,1) tightened by
          a wave-1-tightened source). Prior test's wave 2 was
          fully degenerate.
       2. `updates` dict has THREE entries across two waves
          (vs. one entry in the prior test).
       3. Pruning manifests as push-without-pop; is_bounded
          appears on the orphan push.
       4. Admissibility preserved under multi-wave propagation
          — search still finds cost 7 via a different path
          ((0,1)→(1,1)→(2,1)→...) than the un-propagated run.
    ========================================================================
    """
    def sc(r: int, c: int) -> StateCell:
        return StateCell(key=CellMap(row=r, col=c))

    problem = ProblemGrid.Factory.grid_4x4_obstacle()
    goal = problem.goal
    h = HBounded(
        base=HCallable(fn=lambda s: float(s.distance(goal))),
        bounds={sc(0, 0): 7.0},   # seed = start, tight h*=7
    )
    algo = AStar(problem=problem, h=h, is_recording=True)

    # Pre-propagation: only seed (0,0) is bounded.
    assert h.is_bounded(state=sc(0, 0)) is True
    assert h.is_bounded(state=sc(0, 1)) is False

    updates = algo.propagate_pathmax(depth=2)
    assert updates == {
        sc(0, 1): 6.0,
        sc(1, 0): 6.0,
        sc(1, 1): 5.0,
    }
    # Post-propagation: 4 states bounded (seed + 3 propagated).
    assert h.is_bounded(state=sc(0, 0)) is True
    assert h.is_bounded(state=sc(0, 1)) is True
    assert h.is_bounded(state=sc(1, 0)) is True
    assert h.is_bounded(state=sc(1, 1)) is True
    # Non-propagated states remain unbounded.
    assert h.is_bounded(state=sc(2, 1)) is False
    assert h.is_bounded(state=sc(2, 0)) is False

    sol = algo.run()
    assert sol.cost == 7.0

    actual = [_normalize(e) for e in algo.recorder.events]
    expected = [
        # Propagate events — wave 1 tightens (0,1) and (1,0);
        # wave 2 tightens (1,1) via the lexically-smaller
        # source (0,1) (deterministic via sorted(sources)).
        {'type': 'propagate', 'state': (0, 1),
         'parent': (0, 0), 'h_parent': 7.0, 'h': 6.0},
        {'type': 'propagate', 'state': (1, 0),
         'parent': (0, 0), 'h_parent': 7.0, 'h': 6.0},
        {'type': 'propagate', 'state': (1, 1),
         'parent': (0, 1), 'h_parent': 6.0, 'h': 5.0},
        # Search events (21 — 1 pruned vs. 22 baseline).
        {'type': 'push', 'state': (0, 0), 'g': 0, 'parent': None,
         'h': 7.0, 'f': 7.0, 'is_bounded': True},
        {'type': 'pop',  'state': (0, 0), 'g': 0,
         'h': 7.0, 'f': 7.0, 'is_bounded': True},
        {'type': 'push', 'state': (0, 1), 'g': 1, 'parent': (0, 0),
         'h': 6.0, 'f': 7.0, 'is_bounded': True},
        {'type': 'push', 'state': (1, 0), 'g': 1, 'parent': (0, 0),
         'h': 6.0, 'f': 7.0, 'is_bounded': True},
        {'type': 'pop',  'state': (0, 1), 'g': 1,
         'h': 6.0, 'f': 7.0, 'is_bounded': True},
        {'type': 'push', 'state': (1, 1), 'g': 2, 'parent': (0, 1),
         'h': 5.0, 'f': 7.0, 'is_bounded': True},
        {'type': 'pop',  'state': (1, 1), 'g': 2,
         'h': 5.0, 'f': 7.0, 'is_bounded': True},
        {'type': 'push', 'state': (2, 1), 'g': 3, 'parent': (1, 1),
         'h': 4.0, 'f': 7.0},
        {'type': 'pop',  'state': (2, 1), 'g': 3,
         'h': 4.0, 'f': 7.0},
        {'type': 'push', 'state': (2, 2), 'g': 4, 'parent': (2, 1),
         'h': 3.0, 'f': 7.0},
        {'type': 'push', 'state': (3, 1), 'g': 4, 'parent': (2, 1),
         'h': 5.0, 'f': 9.0},
        {'type': 'push', 'state': (2, 0), 'g': 4, 'parent': (2, 1),
         'h': 5.0, 'f': 9.0},
        {'type': 'pop',  'state': (2, 2), 'g': 4,
         'h': 3.0, 'f': 7.0},
        {'type': 'push', 'state': (2, 3), 'g': 5, 'parent': (2, 2),
         'h': 2.0, 'f': 7.0},
        {'type': 'push', 'state': (3, 2), 'g': 5, 'parent': (2, 2),
         'h': 4.0, 'f': 9.0},
        {'type': 'pop',  'state': (2, 3), 'g': 5,
         'h': 2.0, 'f': 7.0},
        {'type': 'push', 'state': (1, 3), 'g': 6, 'parent': (2, 3),
         'h': 1.0, 'f': 7.0},
        {'type': 'push', 'state': (3, 3), 'g': 6, 'parent': (2, 3),
         'h': 3.0, 'f': 9.0},
        {'type': 'pop',  'state': (1, 3), 'g': 6,
         'h': 1.0, 'f': 7.0},
        {'type': 'push', 'state': (0, 3), 'g': 7, 'parent': (1, 3),
         'h': 0.0, 'f': 7.0},
        {'type': 'pop',  'state': (0, 3), 'g': 7,
         'h': 0.0, 'f': 7.0},
    ]
    assert actual == expected
    assert len(actual) == 24   # 3 propagate + 21 search

    # Propagate events exactly match updates (both count).
    propagate_events = [e for e in actual
                        if e['type'] == 'propagate']
    assert len(propagate_events) == 3
    assert len(propagate_events) == len(updates)
    # Wave-2 event has the wave-1-tightened (0,1) as parent,
    # not the original seed (0,0) — pins the multi-wave chain.
    wave2 = [e for e in propagate_events if e['state'] == (1, 1)]
    assert len(wave2) == 1
    assert wave2[0]['parent'] == (0, 1)
    assert wave2[0]['h_parent'] == 6.0   # (0,1)'s h AFTER wave 1

    # Pruning pin: (1,0) pushed with is_bounded=True but NEVER popped.
    popped_states = {e['state'] for e in actual
                     if e['type'] == 'pop'}
    assert (1, 0) not in popped_states
    push_10 = [e for e in actual
               if e['type'] == 'push' and e['state'] == (1, 0)][0]
    assert push_10.get('is_bounded') is True

    # 7 is_bounded markers total: push+pop of (0,0), (0,1),
    # (1,1); push-only of (1,0).
    bounded = [e for e in actual if e.get('is_bounded')]
    assert len(bounded) == 7
    by_state: dict[tuple, set[str]] = {}
    for e in bounded:
        by_state.setdefault(e['state'], set()).add(e['type'])
    assert by_state == {
        (0, 0): {'push', 'pop'},
        (0, 1): {'push', 'pop'},
        (1, 0): {'push'},             # pruned — no pop
        (1, 1): {'push', 'pop'},
    }

    # is_bounded absent from every other state's events.
    bounded_states = {(0, 0), (0, 1), (1, 0), (1, 1)}
    for e in actual:
        if e['state'] not in bounded_states:
            assert 'is_bounded' not in e

    # No is_cached anywhere.
    for e in actual:
        assert 'is_cached' not in e


def test_recording_hbounded_popped_state_on_grid_4x4_obstacle() -> None:
    """
    ========================================================================
     AStar on grid_4x4_obstacle with Manhattan wrapped in an
     HBounded that bounds **(1,1) at h=5** (tight — h*((1,1))=5
     along the optimal detour). Chosen so the bounded state
     IS popped (not dominated out like (1,0) in the sibling
     test). Verifies `is_bounded=True` appears on BOTH push AND
     pop of the bounded state.

     vs. un-bounded grid_4x4_obstacle (22 events):
       - push (1,1) h=3→5, f=5→7 (bound tightens by 2).
       - Pop order of (1,0) and (1,1) SWAPS: un-bounded pops
         (1,1) first (f=5 with -g=-2 beating (1,0)'s -g=-1);
         bounded pops (1,0) first (f=5 < (1,1) f=7).
       - Event count stays 22 — no pruning, just reordering.

     Pins:
       1. `is_bounded=True` on push (1,1) AND pop (1,1).
       2. is_bounded absent on every other event (including
          every other push/pop of non-bounded states).
       3. is_cached absent everywhere (HBounded.is_perfect=False).
       4. Optimal cost 7 preserved.
    ========================================================================
    """
    def sc(r: int, c: int) -> StateCell:
        return StateCell(key=CellMap(row=r, col=c))

    problem = ProblemGrid.Factory.grid_4x4_obstacle()
    goal = problem.goal
    bounds = {sc(1, 1): 5.0}
    h = HBounded(
        base=HCallable(fn=lambda s: float(s.distance(goal))),
        bounds=bounds,
    )
    algo = AStar(problem=problem, h=h, is_recording=True)
    sol = algo.run()
    assert sol.cost == 7.0

    actual = [_normalize(e) for e in algo.recorder.events]
    expected = [
        {'type': 'push', 'state': (0, 0), 'g': 0, 'parent': None, 'h': 3.0, 'f': 3.0},
        {'type': 'pop',  'state': (0, 0), 'g': 0, 'h': 3.0, 'f': 3.0},
        {'type': 'push', 'state': (0, 1), 'g': 1, 'parent': (0, 0), 'h': 2.0, 'f': 3.0},
        {'type': 'push', 'state': (1, 0), 'g': 1, 'parent': (0, 0), 'h': 4.0, 'f': 5.0},
        {'type': 'pop',  'state': (0, 1), 'g': 1, 'h': 2.0, 'f': 3.0},
        {'type': 'push', 'state': (1, 1), 'g': 2, 'parent': (0, 1), 'h': 5.0, 'f': 7.0, 'is_bounded': True},
        {'type': 'pop',  'state': (1, 0), 'g': 1, 'h': 4.0, 'f': 5.0},
        {'type': 'push', 'state': (2, 0), 'g': 2, 'parent': (1, 0), 'h': 5.0, 'f': 7.0},
        {'type': 'pop',  'state': (1, 1), 'g': 2, 'h': 5.0, 'f': 7.0, 'is_bounded': True},
        {'type': 'push', 'state': (2, 1), 'g': 3, 'parent': (1, 1), 'h': 4.0, 'f': 7.0},
        {'type': 'pop',  'state': (2, 1), 'g': 3, 'h': 4.0, 'f': 7.0},
        {'type': 'push', 'state': (2, 2), 'g': 4, 'parent': (2, 1), 'h': 3.0, 'f': 7.0},
        {'type': 'push', 'state': (3, 1), 'g': 4, 'parent': (2, 1), 'h': 5.0, 'f': 9.0},
        {'type': 'pop',  'state': (2, 2), 'g': 4, 'h': 3.0, 'f': 7.0},
        {'type': 'push', 'state': (2, 3), 'g': 5, 'parent': (2, 2), 'h': 2.0, 'f': 7.0},
        {'type': 'push', 'state': (3, 2), 'g': 5, 'parent': (2, 2), 'h': 4.0, 'f': 9.0},
        {'type': 'pop',  'state': (2, 3), 'g': 5, 'h': 2.0, 'f': 7.0},
        {'type': 'push', 'state': (1, 3), 'g': 6, 'parent': (2, 3), 'h': 1.0, 'f': 7.0},
        {'type': 'push', 'state': (3, 3), 'g': 6, 'parent': (2, 3), 'h': 3.0, 'f': 9.0},
        {'type': 'pop',  'state': (1, 3), 'g': 6, 'h': 1.0, 'f': 7.0},
        {'type': 'push', 'state': (0, 3), 'g': 7, 'parent': (1, 3), 'h': 0.0, 'f': 7.0},
        {'type': 'pop',  'state': (0, 3), 'g': 7, 'h': 0.0, 'f': 7.0},
    ]
    assert actual == expected
    assert len(actual) == 22

    # is_bounded appears on exactly 2 events: push (1,1), pop (1,1).
    bounded = [e for e in actual if e.get('is_bounded')]
    assert len(bounded) == 2
    assert {e['type'] for e in bounded} == {'push', 'pop'}
    assert all(e['state'] == (1, 1) for e in bounded)

    # is_bounded absent from every other event.
    for e in actual:
        if e['state'] != (1, 1):
            assert 'is_bounded' not in e

    # is_cached absent everywhere (HBounded.is_perfect is False).
    for e in actual:
        assert 'is_cached' not in e
