from f_graph.algos.one_to_many.i_1_bfs import BFS_OTM
from f_graph.problems.u_2_one_to_many import UProblemOneToMany, ProblemOneToMany
import pytest


@pytest.fixture
def problem() -> ProblemOneToMany:
    return UProblemOneToMany.gen_3x3()


def test_bfs(problem):
    goal_1, goal_2 = problem.goals
    graph = problem.graph
    bfs = BFS_OTM(problem=problem)
    assert bfs.path.get(goal=goal_1) == [graph[0, 0], graph[0, 1], graph[0, 2]]
    assert bfs.path.get(goal=goal_2) == [graph[0, 0], graph[1, 0], graph[2, 0]]
    assert bfs.data.explored == {graph[0, 0], graph[0, 1], graph[0, 2],
                                 graph[1, 0], graph[1, 1]}
    assert bfs.data.generated.to_list() == [graph[1, 2], graph[2, 1]]
