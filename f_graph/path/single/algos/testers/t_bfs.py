from f_graph.path.single.algos.bfs import BFS
from f_graph.path.single.data.problem import ProblemSingle, NodePath
import pytest


@pytest.fixture
def problem() -> ProblemSingle:
    return ProblemSingle.gen_3x3(type_node=NodePath)


def test_bfs(problem):
    graph = problem.graph
    bfs = BFS(problem=problem)
    solution = bfs.run()
    assert solution.path == [graph[0, 0], graph[0, 1], graph[0, 2],
                             graph[1, 2], graph[2, 2]]
    assert solution.state.explored == {graph[0, 0], graph[0, 1], graph[0, 2],
                                       graph[1, 0], graph[1, 1], graph[1, 2],
                                       graph[2, 0], graph[2, 1]}
    assert not solution.state.generated
    assert solution.state.best == problem.goal


def test_bfs_cache(problem):
    graph = problem.graph.clone()
    graph[1, 2].parent = graph[2, 2]
    cache = {graph[1, 2], graph[2, 2]}
    bfs = BFS(problem=problem, cache=cache)
    solution = bfs.run()
    assert solution.path == [graph[0, 0], graph[0, 1], graph[0, 2],
                             graph[1, 2], graph[2, 2]]
    assert solution.state.explored == {graph[0, 0], graph[0, 1], graph[0, 2],
                                       graph[1, 0], graph[1, 1], graph[2, 0]}
    assert set(solution.state.generated) == {graph[2, 1]}
    assert solution.state.best == graph[1, 2]
