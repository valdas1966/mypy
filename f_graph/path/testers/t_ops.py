from f_graph.path.ops import Ops, Callable, Node
from f_graph.path.generators.g_cache import GenCache
from f_graph.path.generators.g_state import GenState
from f_graph.path.one_to_one.generators.g_problem import GenProblemOneToOne
import pytest


@pytest.fixture
def ops() -> Ops:
    """
    ========================================================================
     Create a test Ops instance.
    ========================================================================
    """
    problem = GenProblemOneToOne.gen_3x3()
    state = GenState.gen_3x3()
    cache = GenCache.gen_3x3()
    heuristic: Callable[[Node], int] = lambda x: 0
    return Ops(problem=problem,
               state=state,
               cache=cache,
               heuristic=heuristic)


def test_generate(ops: Ops) -> None:
    """
    ========================================================================
     Test generate method.
    ========================================================================
    """
    # Non-Cached Node
    node = ops._problem.graph[0, 0]
    ops.generate(node=node, parent=None)
    assert node in ops._state.generated
    assert node.parent is None
    assert node.h == 0
    assert not node.is_cached
    
    # Cached Node
    cached = ops._problem.graph[1, 2]
    ops.generate(node=cached, parent=node)
    assert cached in ops._state.generated 
    assert cached.parent == node
    assert cached.h == 1
    assert cached.is_cached


def test_explore(ops: Ops) -> None:
    """
    ========================================================================
     Test explore method.
    ========================================================================
    """
    node = ops._problem.graph[0, 0]
    child = ops._problem.graph[0, 1]
    ops.explore(node=node)
    assert node in ops._state.explored
    assert child in ops._state.generated
