from f_graph.paths.i_1_one_to_one import PathOneToOne, NodePath
from f_graph.problems.i_2_one_to_one import ProblemOneToOne
from f_graph.graphs.i_1_mutable import GraphMutable
import pytest


@pytest.fixture
def start() -> NodePath:
    return NodePath('START')


@pytest.fixture
def goal(start) -> NodePath:
    node = NodePath('GOAL')
    node.parent = start
    return node


@pytest.fixture
def path(start, goal) -> PathOneToOne:
    graph = GraphMutable()
    problem = ProblemOneToOne(graph=graph, start=start, goal=goal)
    return PathOneToOne(problem=problem)


def test_is_valid(path):
    assert not path
    path.set_valid()
    assert path


def test_get(path, start, goal):
    assert path.get() == [start, goal]
