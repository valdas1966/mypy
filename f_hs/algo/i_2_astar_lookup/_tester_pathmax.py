import pytest

from f_ds.grids.cell.i_1_map import CellMap

from f_hs.algo.i_1_astar import AStar
from f_hs.algo.i_2_astar_lookup import AStarLookup
from f_hs.algo.i_2_astar_lookup._utils import normalize
from f_hs.heuristic.i_0_base._cache_entry import CacheEntry
from f_hs.heuristic.i_1_bounded.main import HBounded
from f_hs.heuristic.i_1_callable.main import HCallable
from f_hs.heuristic.i_1_cached.main import HCached
from f_hs.problem import ProblemSPP
from f_hs.problem.i_1_grid import ProblemGrid
from f_hs.state.i_0_base.main import StateBase
from f_hs.state.i_1_cell.main import StateCell


def test_propagate_pathmax_raises_without_hbounded() -> None:
    """
    ========================================================================
     Calling propagate_pathmax on an AStarLookup whose h has no
     HBounded in its chain raises ValueError — no target
     storage for tightened bounds.
    ========================================================================
    """
    a = StateBase[str](key='A')
    cache = {a: CacheEntry(h_perfect=0, suffix_next=None)}
    h = HCached(base=HCallable(fn=lambda s: 0),
                cache=cache, goal=a)
    algo = AStarLookup(problem=ProblemSPP.Factory.graph_start_is_goal(),
                 h=h)
    assert isinstance(algo, AStarLookup)
    with pytest.raises(ValueError, match='HBounded'):
        algo.propagate_pathmax(depth=2)


def test_propagate_pathmax_grid_4x4_depth_1_from_bounded_seed(
        ) -> None:
    """
    ========================================================================
     Seed HBounded with (1,1)=5. Depth=1 propagates from (1,1)
     to (0,1), (2,1), (1,0). Only (0,1) tightens.
    ========================================================================
    """
    def sc(r: int, c: int) -> StateCell:
        return StateCell(key=CellMap(row=r, col=c))

    problem = ProblemGrid.Factory.grid_4x4_obstacle()
    goal = problem.goal
    h = HBounded(
        base=HCallable(fn=lambda s: s.distance(goal)),
        bounds={sc(1, 1): 5},
    )
    algo = AStarLookup(problem=problem, h=h)
    assert isinstance(algo, AStarLookup)
    updates = algo.propagate_pathmax(depth=1)
    assert updates == {sc(0, 1): 4}
    assert h(sc(0, 1)) == 4
    assert h.is_bounded(state=sc(0, 1)) is True
    assert h.is_bounded(state=sc(2, 1)) is False
    assert h.is_bounded(state=sc(1, 0)) is False


def test_propagate_pathmax_depth_none_runs_to_convergence(
        ) -> None:
    """
    ========================================================================
     `depth=None` (default) propagates until convergence — stops
     when a wave tightens nothing. Seed (0,0)=7: wave 1 tightens
     (0,1) and (1,0); wave 2 tightens (1,1); wave 3 tightens no
     more. Result equals explicit depth=2 for this topology.
    ========================================================================
    """
    def sc(r: int, c: int) -> StateCell:
        return StateCell(key=CellMap(row=r, col=c))

    problem = ProblemGrid.Factory.grid_4x4_obstacle()
    goal = problem.goal
    h = HBounded(
        base=HCallable(fn=lambda s: s.distance(goal)),
        bounds={sc(0, 0): 7},
    )
    algo = AStarLookup(problem=problem, h=h)
    updates = algo.propagate_pathmax()   # depth=None default
    assert updates == {
        sc(0, 1): 6,
        sc(1, 0): 6,
        sc(1, 1): 5,
    }


def test_recording_propagate_wave_events_mark_wave_boundaries(
        ) -> None:
    """
    ========================================================================
     `propagate_wave` events mark the start of each wave that
     runs. Pins:
       1. One wave event per iteration that actually runs.
       2. Depths count from 0 upward.
       3. Emitted BEFORE the wave's attempts (each wave event
          precedes all `propagate` events whose source belongs
          to that wave).
       4. State-less meta-event — no `state` field, no `parent`.
       5. `propagate_pathmax(depth=0)` emits zero wave events
          (loop body never executes).
    ========================================================================
    """
    def sc(r: int, c: int) -> StateCell:
        return StateCell(key=CellMap(row=r, col=c))

    problem = ProblemGrid.Factory.grid_4x4_obstacle()
    goal = problem.goal
    h = HBounded(
        base=HCallable(fn=lambda s: s.distance(goal)),
        bounds={sc(0, 0): 7},
    )
    algo = AStarLookup(problem=problem, h=h, is_recording=True)
    algo.propagate_pathmax()   # depth=None, runs to convergence

    events = [normalize(e) for e in algo.recorder.events]
    wave_events = [e for e in events
                   if e['type'] == 'propagate_wave']
    # Three waves ran: wave 0 seeded by (0,0)=7 (1 source);
    # wave 1 by (0,1) and (1,0) (2 sources); wave 2 by (1,1)
    # (1 source, all targets no-op → loop exits).
    assert [e['depth'] for e in wave_events] == [0, 1, 2]
    assert [e['num_sources'] for e in wave_events] == [1, 2, 1]
    for w in wave_events:
        assert 'state' not in w
        assert 'parent' not in w
        assert 'g' not in w
        assert 'h' not in w
        assert 'num_sources' in w

    # Each wave event precedes its wave's propagate events.
    idx_wave_0 = events.index(wave_events[0])
    idx_wave_1 = events.index(wave_events[1])
    # First propagate (from seed (0,0)) comes after wave 0.
    first_prop = next(i for i, e in enumerate(events)
                      if e['type'] == 'propagate')
    assert idx_wave_0 < first_prop < idx_wave_1

    # depth=0 → no wave events.
    h2 = HBounded(
        base=HCallable(fn=lambda s: s.distance(goal)),
        bounds={sc(0, 0): 7},
    )
    algo2 = AStarLookup(problem=problem, h=h2, is_recording=True)
    algo2.propagate_pathmax(depth=0)
    assert not any(e['type'] == 'propagate_wave'
                   for e in algo2.recorder.events)


def test_propagate_pathmax_depth_zero_is_noop() -> None:
    """
    ========================================================================
     `depth=0` is a valid no-op; returns {} without entering the
     wave loop.
    ========================================================================
    """
    def sc(r: int, c: int) -> StateCell:
        return StateCell(key=CellMap(row=r, col=c))

    problem = ProblemGrid.Factory.grid_4x4_obstacle()
    goal = problem.goal
    h = HBounded(
        base=HCallable(fn=lambda s: s.distance(goal)),
        bounds={sc(0, 0): 7},
    )
    algo = AStarLookup(problem=problem, h=h)
    assert algo.propagate_pathmax(depth=0) == {}


def test_propagate_pathmax_grid_4x4_depth_2_compounds() -> None:
    """
    ========================================================================
     Depth=2 from seed (1,1)=5: wave 1 tightens (0,1) to 4.
     Wave 2 back-edge (0,1)→(1,1) is SKIPPED (last-tightener
     optimisation). (0,1)→(0,0) attempted: no tighten. Final
     updates == {(0,1): 4}.
    ========================================================================
    """
    def sc(r: int, c: int) -> StateCell:
        return StateCell(key=CellMap(row=r, col=c))

    problem = ProblemGrid.Factory.grid_4x4_obstacle()
    goal = problem.goal
    h = HBounded(
        base=HCallable(fn=lambda s: s.distance(goal)),
        bounds={sc(1, 1): 5},
    )
    algo = AStarLookup(problem=problem, h=h)
    updates = algo.propagate_pathmax(depth=2)
    assert updates == {sc(0, 1): 4}
    assert h(sc(0, 0)) == 3
    assert h.is_bounded(state=sc(0, 0)) is False
    assert h(sc(1, 1)) == 5


def test_recording_hbounded_after_pathmax_propagation_depth_2(
        ) -> None:
    """
    ========================================================================
     AStarLookup on grid_4x4_obstacle. Seed HBounded at (1,1)=5.
     propagate_pathmax(depth=2). Pins: last-tightener back-edge
     SKIPPED; 4 propagate events (1 tighten + 3 no-ops); search
     yields 22 events with is_bounded flags.
    ========================================================================
    """
    def sc(r: int, c: int) -> StateCell:
        return StateCell(key=CellMap(row=r, col=c))

    problem = ProblemGrid.Factory.grid_4x4_obstacle()
    goal = problem.goal
    h = HBounded(
        base=HCallable(fn=lambda s: s.distance(goal)),
        bounds={sc(1, 1): 5},
    )
    algo = AStarLookup(problem=problem, h=h, is_recording=True)

    updates = algo.propagate_pathmax(depth=2)
    assert updates == {sc(0, 1): 4}
    assert h(sc(0, 1)) == 4
    assert h(sc(1, 1)) == 5

    sol = algo.run()
    assert sol.cost == 7

    actual = [normalize(e) for e in algo.recorder.events]
    expected = [
        # Wave 0 boundary marker + 3 attempts from seed (1,1)=5.
        {'type': 'propagate_wave', 'depth': 0, 'num_sources': 1},
        {'type': 'propagate', 'state': (0, 1), 'parent': (1, 1), 'h_parent': 5, 'h': 4, 'was_improved': True},
        {'type': 'propagate', 'state': (2, 1), 'parent': (1, 1), 'h_parent': 5, 'h': 4, 'was_improved': False},
        {'type': 'propagate', 'state': (1, 0), 'parent': (1, 1), 'h_parent': 5, 'h': 4, 'was_improved': False},
        # Wave 1 boundary + 1 attempt from (0,1)=4 (back-edge to
        # (1,1) SKIPPED).
        {'type': 'propagate_wave', 'depth': 1, 'num_sources': 1},
        {'type': 'propagate', 'state': (0, 0), 'parent': (0, 1), 'h_parent': 4, 'h': 3, 'was_improved': False},
        # Search events (22).
        {'type': 'push', 'state': (0, 0), 'g': 0, 'parent': None, 'h': 3, 'f': 3},
        {'type': 'pop',  'state': (0, 0), 'g': 0, 'h': 3, 'f': 3},
        {'type': 'push', 'state': (0, 1), 'g': 1, 'parent': (0, 0), 'h': 4, 'f': 5, 'is_bounded': True},
        {'type': 'push', 'state': (1, 0), 'g': 1, 'parent': (0, 0), 'h': 4, 'f': 5},
        {'type': 'pop',  'state': (0, 1), 'g': 1, 'h': 4, 'f': 5, 'is_bounded': True},
        {'type': 'push', 'state': (1, 1), 'g': 2, 'parent': (0, 1), 'h': 5, 'f': 7, 'is_bounded': True},
        {'type': 'pop',  'state': (1, 0), 'g': 1, 'h': 4, 'f': 5},
        {'type': 'push', 'state': (2, 0), 'g': 2, 'parent': (1, 0), 'h': 5, 'f': 7},
        {'type': 'pop',  'state': (1, 1), 'g': 2, 'h': 5, 'f': 7, 'is_bounded': True},
        {'type': 'push', 'state': (2, 1), 'g': 3, 'parent': (1, 1), 'h': 4, 'f': 7},
        {'type': 'pop',  'state': (2, 1), 'g': 3, 'h': 4, 'f': 7},
        {'type': 'push', 'state': (2, 2), 'g': 4, 'parent': (2, 1), 'h': 3, 'f': 7},
        {'type': 'push', 'state': (3, 1), 'g': 4, 'parent': (2, 1), 'h': 5, 'f': 9},
        {'type': 'pop',  'state': (2, 2), 'g': 4, 'h': 3, 'f': 7},
        {'type': 'push', 'state': (2, 3), 'g': 5, 'parent': (2, 2), 'h': 2, 'f': 7},
        {'type': 'push', 'state': (3, 2), 'g': 5, 'parent': (2, 2), 'h': 4, 'f': 9},
        {'type': 'pop',  'state': (2, 3), 'g': 5, 'h': 2, 'f': 7},
        {'type': 'push', 'state': (1, 3), 'g': 6, 'parent': (2, 3), 'h': 1, 'f': 7},
        {'type': 'push', 'state': (3, 3), 'g': 6, 'parent': (2, 3), 'h': 3, 'f': 9},
        {'type': 'pop',  'state': (1, 3), 'g': 6, 'h': 1, 'f': 7},
        {'type': 'push', 'state': (0, 3), 'g': 7, 'parent': (1, 3), 'h': 0, 'f': 7},
        {'type': 'pop',  'state': (0, 3), 'g': 7, 'h': 0, 'f': 7},
    ]
    assert actual == expected
    assert len(actual) == 28   # 2 waves + 4 attempts + 22 search

    wave_events = [e for e in actual
                   if e['type'] == 'propagate_wave']
    assert [e['depth'] for e in wave_events] == [0, 1]
    for w in wave_events:
        assert 'state' not in w  # meta-event, state-less

    propagate_events = [e for e in actual
                        if e['type'] == 'propagate']
    assert len(propagate_events) == 4
    tightenings = [e for e in propagate_events
                   if e['was_improved'] is True]
    assert len(tightenings) == 1
    assert tightenings[0]['state'] == (0, 1)
    for p in propagate_events:
        assert 'g' not in p
        assert 'f' not in p
        assert 'is_bounded' not in p
        assert 'was_improved' in p
    back_edges = [p for p in propagate_events
                  if p['parent'] == (0, 1) and p['state'] == (1, 1)]
    assert len(back_edges) == 0

    bounded_search = [e for e in actual
                      if e['type'] in ('push', 'pop')
                      and e.get('is_bounded')]
    assert len(bounded_search) == 4
    by_state: dict[tuple, set[str]] = {}
    for e in bounded_search:
        by_state.setdefault(e['state'], set()).add(e['type'])
    assert by_state == {(0, 1): {'push', 'pop'},
                        (1, 1): {'push', 'pop'}}
    for e in actual:
        if e['type'] == 'propagate':
            assert 'is_bounded' not in e
        elif (e['type'] in ('push', 'pop', 'decrease_g')
                and e['state'] not in {(0, 1), (1, 1)}):
            assert 'is_bounded' not in e
    for e in actual:
        assert 'is_cached' not in e


def test_recording_pathmax_multiwave_from_start_seed_prunes_on_grid_4x4(
        ) -> None:
    """
    ========================================================================
     Seed (0,0)=7. Multi-wave propagation with last-tightener
     skip active. 5 propagate events (3 tightenings + 2 no-ops;
     2 back-edges to (0,0) skipped). Search pruned to 21 events.
    ========================================================================
    """
    def sc(r: int, c: int) -> StateCell:
        return StateCell(key=CellMap(row=r, col=c))

    problem = ProblemGrid.Factory.grid_4x4_obstacle()
    goal = problem.goal
    h = HBounded(
        base=HCallable(fn=lambda s: s.distance(goal)),
        bounds={sc(0, 0): 7},
    )
    algo = AStarLookup(problem=problem, h=h, is_recording=True)

    assert h.is_bounded(state=sc(0, 0)) is True
    assert h.is_bounded(state=sc(0, 1)) is False

    updates = algo.propagate_pathmax(depth=2)
    assert updates == {
        sc(0, 1): 6,
        sc(1, 0): 6,
        sc(1, 1): 5,
    }
    assert h.is_bounded(state=sc(0, 0)) is True
    assert h.is_bounded(state=sc(0, 1)) is True
    assert h.is_bounded(state=sc(1, 0)) is True
    assert h.is_bounded(state=sc(1, 1)) is True
    assert h.is_bounded(state=sc(2, 1)) is False
    assert h.is_bounded(state=sc(2, 0)) is False

    sol = algo.run()
    assert sol.cost == 7

    actual = [normalize(e) for e in algo.recorder.events]
    expected = [
        # Wave 0 boundary + 2 attempts from seed (0,0)=7.
        {'type': 'propagate_wave', 'depth': 0, 'num_sources': 1},
        {'type': 'propagate', 'state': (0, 1), 'parent': (0, 0), 'h_parent': 7, 'h': 6, 'was_improved': True},
        {'type': 'propagate', 'state': (1, 0), 'parent': (0, 0), 'h_parent': 7, 'h': 6, 'was_improved': True},
        # Wave 1 boundary + 3 attempts from {(0,1),(1,0)} (back-
        # edges to (0,0) skipped).
        {'type': 'propagate_wave', 'depth': 1, 'num_sources': 2},
        {'type': 'propagate', 'state': (1, 1), 'parent': (0, 1), 'h_parent': 6, 'h': 5, 'was_improved': True},
        {'type': 'propagate', 'state': (1, 1), 'parent': (1, 0), 'h_parent': 6, 'h': 5, 'was_improved': False},
        {'type': 'propagate', 'state': (2, 0), 'parent': (1, 0), 'h_parent': 6, 'h': 5, 'was_improved': False},
        # Search events (21).
        {'type': 'push', 'state': (0, 0), 'g': 0, 'parent': None, 'h': 7, 'f': 7, 'is_bounded': True},
        {'type': 'pop',  'state': (0, 0), 'g': 0, 'h': 7, 'f': 7, 'is_bounded': True},
        {'type': 'push', 'state': (0, 1), 'g': 1, 'parent': (0, 0), 'h': 6, 'f': 7, 'is_bounded': True},
        {'type': 'push', 'state': (1, 0), 'g': 1, 'parent': (0, 0), 'h': 6, 'f': 7, 'is_bounded': True},
        {'type': 'pop',  'state': (0, 1), 'g': 1, 'h': 6, 'f': 7, 'is_bounded': True},
        {'type': 'push', 'state': (1, 1), 'g': 2, 'parent': (0, 1), 'h': 5, 'f': 7, 'is_bounded': True},
        {'type': 'pop',  'state': (1, 1), 'g': 2, 'h': 5, 'f': 7, 'is_bounded': True},
        {'type': 'push', 'state': (2, 1), 'g': 3, 'parent': (1, 1), 'h': 4, 'f': 7},
        {'type': 'pop',  'state': (2, 1), 'g': 3, 'h': 4, 'f': 7},
        {'type': 'push', 'state': (2, 2), 'g': 4, 'parent': (2, 1), 'h': 3, 'f': 7},
        {'type': 'push', 'state': (3, 1), 'g': 4, 'parent': (2, 1), 'h': 5, 'f': 9},
        {'type': 'push', 'state': (2, 0), 'g': 4, 'parent': (2, 1), 'h': 5, 'f': 9},
        {'type': 'pop',  'state': (2, 2), 'g': 4, 'h': 3, 'f': 7},
        {'type': 'push', 'state': (2, 3), 'g': 5, 'parent': (2, 2), 'h': 2, 'f': 7},
        {'type': 'push', 'state': (3, 2), 'g': 5, 'parent': (2, 2), 'h': 4, 'f': 9},
        {'type': 'pop',  'state': (2, 3), 'g': 5, 'h': 2, 'f': 7},
        {'type': 'push', 'state': (1, 3), 'g': 6, 'parent': (2, 3), 'h': 1, 'f': 7},
        {'type': 'push', 'state': (3, 3), 'g': 6, 'parent': (2, 3), 'h': 3, 'f': 9},
        {'type': 'pop',  'state': (1, 3), 'g': 6, 'h': 1, 'f': 7},
        {'type': 'push', 'state': (0, 3), 'g': 7, 'parent': (1, 3), 'h': 0, 'f': 7},
        {'type': 'pop',  'state': (0, 3), 'g': 7, 'h': 0, 'f': 7},
    ]
    assert actual == expected
    assert len(actual) == 28   # 2 waves + 5 attempts + 21 search

    wave_events = [e for e in actual
                   if e['type'] == 'propagate_wave']
    assert [e['depth'] for e in wave_events] == [0, 1]

    propagate_events = [e for e in actual
                        if e['type'] == 'propagate']
    assert len(propagate_events) == 5
    tightenings = [e for e in propagate_events
                   if e['was_improved'] is True]
    failures = [e for e in propagate_events
                if e['was_improved'] is False]
    assert len(tightenings) == 3
    assert len(tightenings) == len(updates)
    assert len(failures) == 2
    for p in propagate_events:
        assert 'is_bounded' not in p
    wave2_tighten = [e for e in tightenings
                     if e['state'] == (1, 1)]
    assert len(wave2_tighten) == 1
    assert wave2_tighten[0]['parent'] == (0, 1)
    assert wave2_tighten[0]['h_parent'] == 6
    ww_11_from_10 = [e for e in propagate_events
                     if e['state'] == (1, 1)
                     and e['parent'] == (1, 0)]
    assert len(ww_11_from_10) == 1
    assert ww_11_from_10[0]['was_improved'] is False
    assert ww_11_from_10[0]['h'] == 5
    back_edges_to_00 = [p for p in propagate_events
                        if p['state'] == (0, 0)]
    assert len(back_edges_to_00) == 0

    popped_states = {e['state'] for e in actual
                     if e['type'] == 'pop'}
    assert (1, 0) not in popped_states
    push_10 = [e for e in actual
               if e['type'] == 'push' and e['state'] == (1, 0)][0]
    assert push_10.get('is_bounded') is True

    bounded_search = [e for e in actual
                      if e['type'] in ('push', 'pop')
                      and e.get('is_bounded')]
    assert len(bounded_search) == 7
    by_state: dict[tuple, set[str]] = {}
    for e in bounded_search:
        by_state.setdefault(e['state'], set()).add(e['type'])
    assert by_state == {
        (0, 0): {'push', 'pop'},
        (0, 1): {'push', 'pop'},
        (1, 0): {'push'},
        (1, 1): {'push', 'pop'},
    }
    bounded_states = {(0, 0), (0, 1), (1, 0), (1, 1)}
    for e in actual:
        if (e['type'] in ('push', 'pop', 'decrease_g')
                and e['state'] not in bounded_states):
            assert 'is_bounded' not in e
    for e in actual:
        assert 'is_cached' not in e
