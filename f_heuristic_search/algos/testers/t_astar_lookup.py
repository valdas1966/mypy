from f_heuristic_search.algos.a_star_lookup import AStarLookup
from f_heuristic_search.problem_types.spp import SPP
from f_data_structure.graphs.i_0_grid import GraphGrid as Graph


def test_set_heuristics():
    graph = Graph(rows=3, type_node=Node)
    start = graph[0][0]
    goal = graph[1][1]
    spp = SPP(graph, start, goal)
    lookup = {goal: 9}
    astar = AStarLookup(spp, lookup)
    astar._set_heuristics(node=start)
    astar._set_heuristics(node=goal)
    assert start.h == 2
    assert goal.h == 9

def test_run():
    graph = Graph(rows=4, type_node=NodeFCell)
    graph.make_invalid([(0, 2), (1, 2), (2, 2)])
    start = graph[0][1]
    goal = graph[0][3]
    spp = SPP(graph, start, goal)
    astar = AStar(spp)
    astar.run()




