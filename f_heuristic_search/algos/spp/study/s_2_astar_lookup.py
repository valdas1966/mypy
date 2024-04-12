from f_heuristic_search.problem_types.spp.i_2_lookup import SPPLookup as SPP
from f_data_structure.graphs.i_1_grid import GraphGrid as Graph
from f_heuristic_search.nodes.i_3_f_cell import NodeFCell
from f_heuristic_search.algos.spp.i_2_astar_lookup import AStarLookup


def get_graph_start_goal():
    graph = Graph.from_shape(rows=4, type_node=NodeFCell)
    tuples = [(0, 2), (1, 2)]
    graph.make_invalid(tuples=tuples)
    start = graph[0][1]
    goal = graph[0][3]
    return graph, start, goal


def run_without_lookup():
    graph, start, goal = get_graph_start_goal()
    spp = SPP(graph, start, goal)
    astar = AStarLookup(spp=spp)
    astar.run()
    print(astar.path_optimal())
    print(len(astar.expanded))

def run_with_lookup():
    graph, start, goal = get_graph_start_goal()
    lookup = {graph[2][1]: [graph[2][2], graph[2][3], graph[1][3], graph[0][3]]}
    spp = SPP(graph=graph, start=start, goal=goal, lookup=lookup)
    astar = AStarLookup(spp=spp)
    astar.run()
    print(astar.path_optimal())
    print(len(astar.expanded))


run_without_lookup()
run_with_lookup()