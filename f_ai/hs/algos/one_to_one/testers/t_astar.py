from f_graph.path_finding.generators.gen_problem import UProblemOTO
from f_ai.hs.algos.u_algos import UAlgos, Node


def test():
    problem = UProblemOTO.gen_3x3(type_node=Node)
    graph = problem.graph
    astar = UAlgos.astar(problem=problem)
    assert astar.get_path() == [graph[0, 0], graph[0, 1], graph[0, 2],
                                graph[1, 2], graph[2, 2]]
    assert len(astar._data.explored) == 4
