"""
===============================================================================
 Tests for u_cluster_pool.sample_pool -- the pure (no-Drive) core. Uses an
 in-memory GridMap; the global RNG is seeded explicitly per case.
===============================================================================
"""
import random

from f_ds.grids import GridMap

from f_hs.experiments.u_cluster_pool import sample_pool, _CSV_COLUMNS


def test_count() -> None:
    """
    ========================================================================
     Sampling n single-cell clusters yields exactly n rows.
    ========================================================================
    """
    grid = GridMap.Factory.four_without_obstacles()

    actual = len(list(sample_pool(grids=[grid], steps=0,
                                  min_cells=1, n=5)))

    expected = 5

    assert actual == expected


def test_columns() -> None:
    """
    ========================================================================
     Each row carries exactly the shared CSV schema keys.
    ========================================================================
    """
    grid = GridMap.Factory.four_without_obstacles()

    actual = set(next(sample_pool(grids=[grid], steps=0,
                                  min_cells=1, n=1)).keys())

    expected = set(_CSV_COLUMNS)

    assert actual == expected


def test_single_cell_size() -> None:
    """
    ========================================================================
     steps=0 yields single-cell clusters (cells == 1).
    ========================================================================
    """
    grid = GridMap.Factory.four_without_obstacles()

    actual = next(sample_pool(grids=[grid], steps=0,
                              min_cells=1, n=1))['cells']

    expected = 1

    assert actual == expected


def test_seed_reproducible() -> None:
    """
    ========================================================================
     Same global seed -> identical pool (centers reproduce).
    ========================================================================
    """
    grid = GridMap.Factory.four_without_obstacles()

    random.seed(0)
    a = list(sample_pool(grids=[grid], steps=0, min_cells=1, n=5))
    random.seed(0)
    b = list(sample_pool(grids=[grid], steps=0, min_cells=1, n=5))

    assert a == b


def test_skips_infeasible() -> None:
    """
    ========================================================================
     An unreachable min_cells floor skips every sample (0 rows), never
     raises.
    ========================================================================
    """
    grid = GridMap.Factory.four_without_obstacles()

    actual = len(list(sample_pool(grids=[grid], steps=0,
                                  min_cells=999, n=3, max_tries=5)))

    expected = 0

    assert actual == expected
