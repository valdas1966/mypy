from f_graph.problems.u_2_one_to_one import UProblemOTO
from f_graph.algos.one_to_one.i_1_bfs import BFS
from f_ai.hs.algos.u_algos_grid import UAlgosGrid, NodeFCell


def test_random():
    problem = UProblemOTO.generate(rows=100, pct_valid=75, type_node=NodeFCell)
    bfs = BFS(problem=problem)
    astar = UAlgosGrid.astar(problem=problem)
    assert bfs.path.get() == astar.path.get()

