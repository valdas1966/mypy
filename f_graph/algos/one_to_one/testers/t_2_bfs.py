from f_graph.path.single.generators.gen_problem import UProblemOTO
from f_graph.algos.i_1_bfs import BFS


def test():
    problem = UProblemOTO.gen_3x3()
    graph = problem.graph
    bfs = BFS(problem)
    assert bfs.get_path() == [graph[0, 0], graph[0, 1], graph[0, 2],
                              graph[1, 2], graph[2, 2]]
    assert len(bfs._data.explored) == 8

