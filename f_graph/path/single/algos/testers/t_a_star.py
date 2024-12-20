from f_graph.path.single.algos.a_star import AStar, Problem
import pytest


@pytest.fixture
def problem() -> Problem:
    return Problem.gen_3x3()


def test_a_star(problem):
    graph = problem.graph

