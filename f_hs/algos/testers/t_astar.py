from f_graph.problems.i_2_one_to_one import ProblemOneToOne
from f_graph.graphs.i_1_grid import GraphGrid, Grid
from f_hs.heuristics.i_1_manhattan import HeuristicsManhattan
from f_hs.nodes.i_1_f_cell import NodeFCell
from f_hs.algos.a_star import AStar


def test():
    grid = Grid(3)
    graph = GraphGrid(grid=grid, type_node=NodeFCell)
    start = graph[0, 0]
    goal = graph[2, 2]
    problem = ProblemOneToOne(graph=graph, start=start, goal=goal)
    heuristics = HeuristicsManhattan(problem=problem)
    astar = AStar(problem=problem, heuristics=heuristics.eval)
    assert astar.path.get() == [graph[0, 0], graph[0, 1], graph[0, 2],
                                graph[1, 2], graph[2, 2]]
    assert len(astar.data.explored) == 4


