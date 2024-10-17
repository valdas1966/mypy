from f_graph.problems.i_2_one_to_one import ProblemOneToOne
from f_graph.graphs.i_1_grid import GraphGrid, Grid
from f_ai.hs.heuristics.i_1_manhattan import HeuristicsManhattan
from f_ai.hs.nodes.i_1_f_cell import NodeFCell
from f_ai.hs.algos.one_to_one.a_star import AStar
from f_graph.problems.u_2_one_to_one import UProblemOTO


def test():
    problem = UProblemOTO.gen_3x3(type_node=NodeFCell)
    graph = problem.graph
    heuristics = HeuristicsManhattan(distance=problem.graph.distance,
                                     goal=problem.goal)
    astar = AStar(problem=problem, heuristics=heuristics)
    assert problem.goal.path_from_root() == [graph[0, 0], graph[0, 1],
                                             graph[0, 2],
                                             graph[1, 2], graph[2, 2]]
    assert len(astar.data.explored) == 4
