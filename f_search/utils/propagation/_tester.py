from f_search.utils.propagation import Propagation
from f_ds.grids import GridMap as Grid


def test_single_source() -> None:
    """
    ========================================================================
     Test propagation from a single source with depth=2.
    ========================================================================
    """
    prop = Propagation.Factory.single_source()
    result = prop.run()
    grid = Grid.Factory.four_without_obstacles()
    received = {s.key: v for s, v in result.items()}
    # (0,0)=3:
    # depth=1: (0,1)=2, (1,0)=2
    # depth=2: (0,2)=1, (1,1)=1, (2,0)=1
    expected = {grid[0][1]: 2, grid[1][0]: 2,
                grid[0][2]: 1, grid[1][1]: 1, grid[2][0]: 1}
    assert received == expected


def test_multi_source() -> None:
    """
    ========================================================================
     Test that max value wins when multiple sources reach same state.
    ========================================================================
    """
    prop = Propagation.Factory.multi_source()
    result = prop.run()
    grid = Grid.Factory.four_without_obstacles()
    received = {s.key: v for s, v in result.items()}
    # (0,0)=2 → (0,1)=1, (1,0)=1
    # (0,3)=4 → (0,2)=3, (1,3)=3
    expected = {grid[0][1]: 1, grid[1][0]: 1,
                grid[0][2]: 3, grid[1][3]: 3}
    assert received == expected


def test_with_prune() -> None:
    """
    ========================================================================
     Test that pruning skips states below threshold.
    ========================================================================
    """
    prop = Propagation.Factory.single_source_with_prune()
    result = prop.run()
    grid = Grid.Factory.four_without_obstacles()
    received = {s.key: v for s, v in result.items()}
    # (0,0)=3 → (0,1)=2 > 1 kept, (1,0)=2 > 1 kept
    # depth=2: (0,2)=1 <= 1 pruned, (1,1)=1 <= 1 pruned,
    #  (2,0)=1 <= 1 pruned
    expected = {grid[0][1]: 2, grid[1][0]: 2}
    assert received == expected


def test_depth_zero() -> None:
    """
    ========================================================================
     Test that depth=0 returns empty result.
    ========================================================================
    """
    prop = Propagation.Factory.single_source_depth_zero()
    result = prop.run()
    assert result == {}
