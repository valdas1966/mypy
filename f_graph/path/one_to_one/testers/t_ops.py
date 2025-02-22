from f_graph.path.one_to_one.generators.g_ops import GenOps
from f_graph.path.one_to_one.ops import OpsOneToOne, TypeCounter
import pytest


def test_generate_from_explored() -> None:
    """
    ========================================================================
     Test generate method with Explored-Cache.
    ========================================================================
    """
    ops = GenOps.first_row_branch_3x3_explored()
    start = ops._problem.start
    ops.generate(node=start, parent=None)
    assert start in ops._state.generated
    assert start.is_cached
    assert start.h == 0


def test_generate_from_path() -> None:
    """
    =========================================================================
     Test Generate-Node method with Path-Cache.
    =========================================================================
    """
    ops = GenOps.first_row_branch_3x3_path()
    start = ops._problem.start
    ops.generate(node=start, parent=None)
    assert start in ops._state.generated
    assert start.is_cached
    assert start.h == 2


def test_generate_boundary_4x4() -> None:
    """
    ========================================================================
     Test generate method with Boundary-Cache.
    ========================================================================
    """
    ops = GenOps.boundary_4x4()
    graph = ops._problem.graph
    start = graph[2, 2]
    ops.generate(node=start, parent=None)
    assert start in ops._state.generated
    assert not start.is_cached
    assert start.h == 6
