import os
import pickle
import tempfile

import pytest

from f_hs.problem.i_1_grid import ProblemGrid
from f_ds.grids.grid.map import GridMap


def _make_problem(grid_name: str = 'g1') -> ProblemGrid:
    """
    ============================================================================
     Build a 4x4 ProblemGrid with a small obstacle, a named Grid.
    ============================================================================
    """
    grid = GridMap(rows=4, cols=4, name=grid_name)
    grid[1][2].set_invalid()
    return ProblemGrid(grid=grid,
                       start=grid[0][0],
                       goal=grid[3][3],
                       name=f'p_{grid_name}')


def test_pickle_roundtrip_is_detached() -> None:
    """
    ========================================================================
     Direct pickle.dumps/loads produces a DETACHED ProblemGrid.
    ========================================================================
    """
    p = _make_problem()
    data = pickle.dumps(p)
    q: ProblemGrid = pickle.loads(data)
    assert not q.is_attached
    assert q.grid_name == p.grid_name
    assert q.start_rc == p.start_rc
    assert q.goal_rc == p.goal_rc


def test_pickle_light_size() -> None:
    """
    ========================================================================
     Detached pickle is much smaller than the attached one on a non-
     trivial grid (sanity check that grid + states are dropped).
    ========================================================================
    """
    grid = GridMap(rows=20, cols=20, name='big')
    p_attached = ProblemGrid(grid=grid,
                             start=grid[0][0],
                             goal=grid[19][19])
    # Force attachment before measuring "heavy" size — clone and force
    # state dict into __getstate__-untouched form by pickling __dict__.
    heavy = pickle.dumps(p_attached.__dict__)
    light = pickle.dumps(p_attached)
    assert len(light) < len(heavy) / 2


def test_detached_raises_on_grid_access() -> None:
    """
    ========================================================================
     Accessing `grid` on a detached Problem raises RuntimeError.
    ========================================================================
    """
    p = _make_problem()
    p.detach()
    with pytest.raises(RuntimeError):
        _ = p.grid


def test_attach_restores_successors() -> None:
    """
    ========================================================================
     After detach + attach, successors() yields the same (row, col) set.
    ========================================================================
    """
    p = _make_problem()
    children_before = {s.rc for s in p.successors(p.start)}
    p.detach()
    grid = GridMap(rows=4, cols=4, name='g1')
    grid[1][2].set_invalid()
    p.attach(grid=grid)
    children_after = {s.rc for s in p.successors(p.start)}
    assert children_before == children_after


def test_attach_name_mismatch_raises() -> None:
    """
    ========================================================================
     Attaching a Grid whose `name` differs from the Problem's recorded
     grid_name raises ValueError.
    ========================================================================
    """
    p = _make_problem(grid_name='g1')
    p.detach()
    other = GridMap(rows=4, cols=4, name='other')
    with pytest.raises(ValueError):
        p.attach(grid=other)


def test_store_save_load_roundtrip() -> None:
    """
    ========================================================================
     Store.save + Store.load yield bound Problems equivalent to the
     originals (start, goal, successors).
    ========================================================================
    """
    p1 = _make_problem(grid_name='g1')
    p2 = _make_problem(grid_name='g2')
    grids = {'g1': p1.grid, 'g2': p2.grid}
    with tempfile.TemporaryDirectory() as d:
        pp = os.path.join(d, 'problems.pkl')
        pg = os.path.join(d, 'grids.pkl')
        ProblemGrid.Store.save(problems=[p1, p2],
                               grids=grids,
                               path_problems=pp,
                               path_grids=pg)
        loaded, loaded_grids = ProblemGrid.Store.load(path_problems=pp,
                                                     path_grids=pg)
    assert len(loaded) == 2
    for orig, back in zip([p1, p2], loaded):
        assert back.is_attached
        assert back.start_rc == orig.start_rc
        assert back.goal_rc == orig.goal_rc
        orig_children = {s.rc for s in orig.successors(orig.start)}
        back_children = {s.rc for s in back.successors(back.start)}
        assert orig_children == back_children


def test_store_shares_state_cache_across_problems() -> None:
    """
    ========================================================================
     Two Problems on the same Grid share a single `_states` dict after
     Store.load — zero duplicated StateCell objects.
    ========================================================================
    """
    grid = GridMap(rows=5, cols=5, name='shared')
    p1 = ProblemGrid(grid=grid, start=grid[0][0], goal=grid[4][4],
                     name='p1')
    p2 = ProblemGrid(grid=grid, start=grid[0][0], goal=grid[2][2],
                     name='p2')
    with tempfile.TemporaryDirectory() as d:
        pp = os.path.join(d, 'problems.pkl')
        pg = os.path.join(d, 'grids.pkl')
        ProblemGrid.Store.save(problems=[p1, p2],
                               grids={'shared': grid},
                               path_problems=pp,
                               path_grids=pg)
        loaded, _ = ProblemGrid.Store.load(path_problems=pp,
                                           path_grids=pg)
    q1, q2 = loaded
    # Same dict object — shared cache
    assert q1._states is q2._states
    # Both refer to the same loaded Grid
    assert q1._grid is q2._grid


def test_store_unbound_mode() -> None:
    """
    ========================================================================
     Store.load(bind=False) returns detached Problems. Caller may bind
     selectively via Store.bind().
    ========================================================================
    """
    p = _make_problem()
    grids = {'g1': p.grid}
    with tempfile.TemporaryDirectory() as d:
        pp = os.path.join(d, 'problems.pkl')
        pg = os.path.join(d, 'grids.pkl')
        ProblemGrid.Store.save(problems=[p],
                               grids=grids,
                               path_problems=pp,
                               path_grids=pg)
        loaded, g = ProblemGrid.Store.load(path_problems=pp,
                                           path_grids=pg,
                                           bind=False)
    assert not loaded[0].is_attached
    ProblemGrid.Store.bind(problems=loaded, grids=g)
    assert loaded[0].is_attached


def test_store_missing_grid_raises() -> None:
    """
    ========================================================================
     Saving a Problem referencing a grid_name absent from `grids`
     raises ValueError.
    ========================================================================
    """
    p = _make_problem(grid_name='g1')
    with tempfile.TemporaryDirectory() as d:
        pp = os.path.join(d, 'problems.pkl')
        pg = os.path.join(d, 'grids.pkl')
        with pytest.raises(ValueError):
            ProblemGrid.Store.save(problems=[p],
                                   grids={},
                                   path_problems=pp,
                                   path_grids=pg)


def test_store_grid_key_mismatch_raises() -> None:
    """
    ========================================================================
     Saving with a grids dict whose key disagrees with grid.name raises.
    ========================================================================
    """
    p = _make_problem(grid_name='g1')
    with tempfile.TemporaryDirectory() as d:
        pp = os.path.join(d, 'problems.pkl')
        pg = os.path.join(d, 'grids.pkl')
        with pytest.raises(ValueError):
            ProblemGrid.Store.save(problems=[p],
                                   grids={'wrong_key': p.grid},
                                   path_problems=pp,
                                   path_grids=pg)


def test_key_stable_across_detach() -> None:
    """
    ========================================================================
     Problem.key and hash are stable before / after detach, enabling the
     Problem to be used in sets / dicts even when detached.
    ========================================================================
    """
    p = _make_problem()
    k_before = p.key
    h_before = hash(p)
    p.detach()
    assert p.key == k_before
    assert hash(p) == h_before
