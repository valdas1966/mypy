from f_graph.old_path.algos.one_to_one.problem import ProblemOneToOne as Problem
from f_graph.old_path.algos.one_to_one.generators.g_problem import GenProblemOneToOne
import pytest


@pytest.fixture
def problem() -> Problem:
    return GenProblemOneToOne.gen_3x3()


def test_clone(problem: Problem) -> None:
    """
    ========================================================================
     Test that clone creates an equal but separate problem.
    ========================================================================
    """
    clone = problem.clone()
    assert clone == problem
    assert clone is not problem


def test_reverse(problem: Problem) -> None:
    """
    ========================================================================
     Test that reverse swaps start and goal old_nodes.
    ========================================================================
    """
    reversed_problem = problem.reverse()
    assert reversed_problem.start == problem.goal
    assert reversed_problem.goal == problem.start
