from f_ai.hs.nodes.i_1_f_cell import NodeFCell
from f_ai.hs.algos.one_to_one.a_star import AStar
from f_graph.problems.u_2_one_to_one import UProblemOTO
from functools import partial


def test():
    problem = UProblemOTO.gen_3x3(type_node=NodeFCell)
    graph = problem.graph
    heuristics = partial(problem.graph.distance, node_b=problem.goal)
    astar = AStar(problem=problem, heuristics=heuristics)
    assert astar.get_path() == [graph[0, 0], graph[0, 1], graph[0, 2],
                                graph[1, 2], graph[2, 2]]
    assert len(astar._data.explored) == 4
