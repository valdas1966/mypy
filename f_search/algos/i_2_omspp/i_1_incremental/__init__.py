from f_core.imports import ULazy

ULazy.install(globals(), {
    'AStarIncremental': 'f_search.algos.i_2_omspp.i_1_incremental.astar:AStarIncremental',
    'BFSIncremental': 'f_search.algos.i_2_omspp.i_1_incremental.bfs:BFSIncremental',
    'DijkstraIncremental': 'f_search.algos.i_2_omspp.i_1_incremental.dijkstra:DijkstraIncremental',
    'AStarIncrementalBackward': 'f_search.algos.i_2_omspp.i_1_incremental.astar_backward:AStarIncrementalBackward',
})
