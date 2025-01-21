from f_graph.path.one_to_one.solution import SolutionOneToOne, StatsPath, Node
from f_graph.path.one_to_one.generators.g_problem import GenProblemOneToOne
from f_graph.path.one_to_one.generators.g_state import GenStateOneToOne
from f_graph.path.one_to_one.generators.g_cache import GenCache
import pytest


def test_solution_3x3() -> None:
    """
    ========================================================================
     Test that solution_3x3 creates a solution for a 3x3 problem.
    ========================================================================
    """
    problem = GenProblemOneToOne.gen_3x3()
    cache = GenCache.gen_3x3()
    state = GenStateOneToOne.gen_3x3()
    stats = StatsPath(elapsed=10, explored=20)
    solution = SolutionOneToOne(is_valid=True, stats=stats, cache=cache
    assert solution == [Node(0, 2), Node(0, 1), Node(1, 1), Node(2, 1), Node(2, 2)]

