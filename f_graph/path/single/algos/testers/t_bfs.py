from f_graph.path.single.algos.bfs import BFS
from f_graph.path.single.data.problem import ProblemSingle, NodePath


def test_bfs():
    problem = ProblemSingle.gen_3x3(type_node=NodePath)
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
