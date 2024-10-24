from f_graph.problems.u_2_one_to_one import UProblemOTO
from f_graph.algos.one_to_one.i_1_bfs import BFS
from f_graph.termination.one_to_one.i_1_cache import TerminationCache


def test():
    problem = UProblemOTO.gen_3x3()
    graph = problem.graph
    bfs = BFS(problem)
    assert problem.goal.path_from_root() == [graph[0, 0], graph[0, 1],
                                             graph[0, 2], graph[1, 2],
                                             graph[2, 2]]
    assert len(bfs.data.explored) == 8

