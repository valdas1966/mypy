from typing import TYPE_CHECKING

from f_core.imports import ULazy

if TYPE_CHECKING:
    from f_search.algos.i_2_omspp.i_0_base import AlgoOMSPP
    from f_search.algos.i_2_omspp.i_1_repeated.astar import AStarRepeated
    from f_search.algos.i_2_omspp.i_1_repeated.astar_backward import AStarRepeatedBackward
    from f_search.algos.i_2_omspp.i_1_aggregative import AStarAggregative
    from f_search.algos.i_2_omspp.i_1_incremental.bfs import BFSIncremental
    from f_search.algos.i_2_omspp.i_1_incremental.astar import AStarIncremental
    from f_search.algos.i_2_omspp.i_1_incremental.dijkstra import DijkstraIncremental
    from f_search.algos.i_2_omspp.i_1_incremental.astar_backward import AStarIncrementalBackward

ULazy.install(globals(), {
    'AlgoOMSPP': 'f_search.algos.i_2_omspp.i_0_base:AlgoOMSPP',
    'AStarRepeated': 'f_search.algos.i_2_omspp.i_1_repeated.astar:AStarRepeated',
    'AStarRepeatedBackward': 'f_search.algos.i_2_omspp.i_1_repeated.astar_backward:AStarRepeatedBackward',
    'AStarAggregative': 'f_search.algos.i_2_omspp.i_1_aggregative:AStarAggregative',
    'BFSIncremental': 'f_search.algos.i_2_omspp.i_1_incremental.bfs:BFSIncremental',
    'AStarIncremental': 'f_search.algos.i_2_omspp.i_1_incremental.astar:AStarIncremental',
    'DijkstraIncremental': 'f_search.algos.i_2_omspp.i_1_incremental.dijkstra:DijkstraIncremental',
    'AStarIncrementalBackward': 'f_search.algos.i_2_omspp.i_1_incremental.astar_backward:AStarIncrementalBackward',
})
