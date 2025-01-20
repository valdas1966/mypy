from f_graph.path.one_to_one.problem import ProblemOneToOne as Problem, Node
from f_graph.path.one_to_one.state import State
from f_ds.queues.i_1_priority import QueuePriority
from f_graph.path.one_to_one.ops import Ops, Callable
import pytest


@pytest.fixture
def problem() -> Problem:
    """
    ========================================================================
     Create a test Problem instance.
    ========================================================================
    """
    return Problem.gen_3x3()


@pytest.fixture
def goal(problem: Problem) -> Node:
    """
    ========================================================================
     Create a test goal node.
    ========================================================================
    """
    return problem.graph[2, 2]


@pytest.fixture
def pre_goal(problem: Problem) -> Node:
    """
    ========================================================================
     Create a test pre-goal node.
    ========================================================================
    """
    return problem.graph[1, 2]


@pytest.fixture
def cache(goal: Node, pre_goal: Node) -> dict[Node, Callable[[], list[Node]]]:
    """
    ========================================================================
     Create a test cache.
    ========================================================================
    """
    return {pre_goal: lambda: [goal]}


@pytest.fixture
def ops(problem: Problem,
         cache: dict[Node, Callable[[], list[Node]]]) -> Ops:
    """
    ========================================================================
     Create a test Ops instance.
    ========================================================================
    """
    state = State(type_queue=QueuePriority)
    heuristic: Callable[[Node], int] = lambda x: 0
    
    return Ops(
        problem=problem,
        state=state,
        cache=cache,
        heuristic=heuristic
    )


def test_init(ops: Ops) -> None:
    """
    ========================================================================
     Test Ops initialization.
    ========================================================================
    """
    assert isinstance(ops._problem, Problem)
    assert isinstance(ops._state, State)
    assert isinstance(ops._cache, dict)
    assert callable(ops._heuristic)


def test_generate(ops: Ops, goal: Node, pre_goal: Node) -> None:
    """
    ========================================================================
     Test generate method.
    ========================================================================
    """
    ops.generate(node=pre_goal, parent=None)
    assert pre_goal.parent is None
    assert pre_goal.h == 1
    assert pre_goal.is_cached
    assert pre_goal in ops._state.generated

    ops.generate(node=goal, parent=pre_goal)
    assert goal.parent == pre_goal
    assert goal.h == 0
    assert not goal.is_cached
    assert goal in ops._state.generated        


def test_explore(ops: Ops, goal: Node) -> None:
    """
    ========================================================================
     Test explore method.
    ========================================================================
    """
    ops.explore(node=goal)
    assert goal in ops._state.explored
