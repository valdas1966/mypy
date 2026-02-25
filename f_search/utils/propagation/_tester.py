from f_search.utils.propagation.main import propagate
from f_search.utils.propagation._factory import Factory


def test_single_source() -> None:
    """
    ========================================================================
     Test propagation from a single source with depth=2.
    ========================================================================
    """
    sources, excluded, successors, grid = Factory.single_source()
    result = propagate(sources=sources,
                       excluded=excluded,
                       successors=successors,
                       depth=2)
    received = {s.key: v for s, v in result.items()}
    # (0,0)=3 → depth=1: (0,1)=2, (1,0)=2
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
    sources, excluded, successors, grid = Factory.multi_source()
    result = propagate(sources=sources,
                       excluded=excluded,
                       successors=successors,
                       depth=1)
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
    sources, excluded, successors, grid = Factory.single_source()
    # Prune states with value <= 2 (only value=2 survives)
    result = propagate(sources=sources,
                       excluded=excluded,
                       successors=successors,
                       depth=2,
                       prune=lambda state: 1)
    received = {s.key: v for s, v in result.items()}
    # (0,0)=3 → (0,1)=2 > 1 kept, (1,0)=2 > 1 kept
    # depth=2: (0,2)=1 <= 1 pruned, (1,1)=1 <= 1 pruned, (2,0)=1 <= 1 pruned
    expected = {grid[0][1]: 2, grid[1][0]: 2}
    assert received == expected


def test_depth_zero() -> None:
    """
    ========================================================================
     Test that depth=0 returns empty result.
    ========================================================================
    """
    sources, excluded, successors, grid = Factory.single_source()
    result = propagate(sources=sources,
                       excluded=excluded,
                       successors=successors,
                       depth=0)
    assert result == {}
