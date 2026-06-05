from typing import TYPE_CHECKING

from f_core.imports import ULazy

if TYPE_CHECKING:
    from f_search.algos.i_1_spp.i_0_base import AlgoSPP
    from f_search.algos.i_1_spp.i_1_astar import AStar
    from f_search.algos.i_1_spp.i_1_bfs import BFS
    from f_search.algos.i_1_spp.i_1_dijkstra import Dijkstra
    from f_search.algos.i_1_spp.i_2_astar_reusable import AStarReusable
    from f_search.algos.i_1_spp.i_3_astar_cached import AStarCached

ULazy.install(globals(), {
    'AlgoSPP': 'f_search.algos.i_1_spp.i_0_base:AlgoSPP',
    'AStar': 'f_search.algos.i_1_spp.i_1_astar:AStar',
    'BFS': 'f_search.algos.i_1_spp.i_1_bfs:BFS',
    'Dijkstra': 'f_search.algos.i_1_spp.i_1_dijkstra:Dijkstra',
    'AStarReusable': 'f_search.algos.i_1_spp.i_2_astar_reusable:AStarReusable',
    'AStarCached': 'f_search.algos.i_1_spp.i_3_astar_cached:AStarCached',
})
