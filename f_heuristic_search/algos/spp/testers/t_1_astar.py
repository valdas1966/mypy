from f_heuristic_search.algos.spp.i_1_astar import AStar, NodeFCell
from f_heuristic_search.problem_types.spp.i_1_heuristics import \
    (SPPHeuristics, GraphGrid as Graph)


def test_astar():
    graph = Graph.from_shape(rows=3, type_node=NodeFCell)
    start = graph[0][0]
    goal = graph[2][2]
    spp = SPPHeuristics(graph=graph, start=start, goal=goal)
    astar = AStar(spp=spp)
    astar.run()
    optimal_path = [start, graph[0][1], graph[0][2], graph[1][2], goal]
    assert astar.optimal_path() == optimal_path
    assert astar.expanded == set(optimal_path)-{goal}
    assert astar.generated == [graph[1][1], graph[1][0]]
