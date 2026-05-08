import pytest

from f_ds.grids.cell.i_1_map import CellMap

from f_hs.algo.i_0_oospp.i_1_astar import AStar
from f_hs.algo.i_0_oospp.i_2_astar_lookup import AStarLookup
from f_hs.algo.u_event_normalize import normalize
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

