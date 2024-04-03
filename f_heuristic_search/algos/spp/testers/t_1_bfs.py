from f_heuristic_search.problem_types.spp.i_0_concrete import SPPConcrete
from f_heuristic_search.algos.spp.i_1_bfs import BFS
from f_data_structure.graphs.i_1_grid import GraphGrid as Graph


def test_bfs():
    graph = Graph.from_shape(rows=3)
    start = graph[0][0]
    goal = graph[2][2]
    spp = SPPConcrete(graph=graph, start=start, goal=goal)
    bfs = BFS(spp=spp)
    bfs.run()
    assert len(bfs.optimal_path()) == 5
    assert len(bfs.expanded) == 8
    assert len(bfs.generated) == 0
