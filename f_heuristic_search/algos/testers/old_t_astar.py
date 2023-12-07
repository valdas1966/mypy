from f_heuristic_search.algos.spp.a_star import AStar
from f_heuristic_search.problem_types.spp import SPP
from f_heuristic_search.domain.grid.node import NodeFCell
from f_data_structure.graphs.i_0_grid import GraphGrid as Graph


def test_run():
    graph = Graph(rows=4, type_node=NodeFCell)
    graph.make_invalid([(0, 2), (1, 2), (2, 2)])
    start = graph[0][1]
    goal = graph[0][3]
    spp = SPP(graph, start, goal)
    astar = AStar(spp)
    astar.run()
    assert [node.to_tuple() for node in astar.optimal_path()] ==\
           [(0, 1), (1, 1), (2, 1), (3, 1), (3, 2), (3, 3), (2, 3), (1, 3),
            (0, 3)]
    assert {node.to_tuple() for node in astar.closed} == \
           {(0, 0), (0, 1), (1, 0), (1, 1), (2, 0), (2, 1), (3, 1), (3, 2),
            (3, 3), (2, 3), (1, 3), (0, 3)}



