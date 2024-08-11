from f_graph.problems.i_2_one_to_one import ProblemOneToOne
from f_graph.graphs.i_1_grid import GraphGrid, Grid
from f_graph.nodes.i_2_g_cell import NodeGCell
from f_graph.algos.ucs import UCS


def test():
    grid = Grid(3)
    graph = GraphGrid(grid=grid, type_node=NodeGCell)
    start = graph[0, 0]
    goal = graph[2, 2]
    problem = ProblemOneToOne(graph=graph, start=start, goal=goal)
    ucs = UCS(problem)
    assert ucs.path.get() == [graph[0, 0], graph[0, 1], graph[0, 2],
                              graph[1, 2], graph[2, 2]]


