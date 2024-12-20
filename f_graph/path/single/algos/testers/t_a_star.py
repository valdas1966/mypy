from f_graph.path.single.algos.a_star import AStar, Problem
import pytest


@pytest.fixture
def problem() -> Problem:
    return Problem.gen_4x4()


def test_a_star(problem):
    graph = problem.graph
    astar = AStar(problem=problem)
    solution = astar.run()
    assert solution.path == [graph[0, 0], graph[0, 1], graph[1, 1], graph[2, 1],
                             graph[2, 2], graph[2, 3], graph[1, 3], graph[0, 3]]
    assert solution.state.explored == {graph[0, 0], graph[0, 1],
                                       graph[1, 0], graph[1, 1], graph[1, 3],
                                       graph[2, 0], graph[2, 1], graph[2, 2],
                                       graph[2, 3]}
    assert set(solution.state.generated) == {graph[3, 0], graph[3, 1],
                                             graph[3, 2], graph[3, 3]}
    assert solution.state.best == problem.goal


def test_a_star_cache(problem):
    graph = problem.graph.clone()


