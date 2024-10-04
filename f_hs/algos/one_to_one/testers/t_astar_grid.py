from f_graph.problems.i_2_one_to_one import ProblemOneToOne
from f_graph.graphs.u_1_grid import UGraphGrid
from f_graph.algos.one_to_one.i_1_bfs import BFS
from f_hs.algos.one_to_one.a_star_grid import AStarGrid, NodeFCell


def test_random():
    graph = UGraphGrid.generate(rows=100, pct_valid=75, type_node=NodeFCell)
    start, goal = graph.sample(size=2)
    problem = ProblemOneToOne(graph=graph, start=start, goal=goal)
    bfs = BFS(problem=problem)
    astar = AStarGrid(problem=problem)
    assert bfs.path.get() == astar.path.get()

