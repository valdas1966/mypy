from typing import TYPE_CHECKING

from f_core.imports import ULazy

if TYPE_CHECKING:
    from f_search.algos.i_2_omspp.i_1_incremental.astar import AStarIncremental
    from f_search.algos.i_2_omspp.i_1_incremental.bfs import BFSIncremental
    from f_search.algos.i_2_omspp.i_1_incremental.dijkstra import DijkstraIncremental
    from f_search.algos.i_2_omspp.i_1_incremental.astar_backward import AStarIncrementalBackward

ULazy.install(globals(), {
    'AStarIncremental': 'f_search.algos.i_2_omspp.i_1_incremental.astar:AStarIncremental',
    'BFSIncremental': 'f_search.algos.i_2_omspp.i_1_incremental.bfs:BFSIncremental',
    'DijkstraIncremental': 'f_search.algos.i_2_omspp.i_1_incremental.dijkstra:DijkstraIncremental',
    'AStarIncrementalBackward': 'f_search.algos.i_2_omspp.i_1_incremental.astar_backward:AStarIncrementalBackward',
})
