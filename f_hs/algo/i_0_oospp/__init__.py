from typing import TYPE_CHECKING

from f_core.imports import ULazy

if TYPE_CHECKING:
    from f_hs.algo.i_0_oospp.i_0_base import AlgoSPP
    from f_hs.algo.i_0_oospp.i_0_base import SearchStateSPP
    from f_hs.algo.i_0_oospp.i_1_bfs import BFS
    from f_hs.algo.i_0_oospp.i_1_astar import AStar
    from f_hs.algo.i_0_oospp.i_2_astar_lookup import AStarLookup
    from f_hs.algo.i_0_oospp.i_3_astar_bpmx import AStarBPMX
    from f_hs.algo.i_0_oospp.i_2_dijkstra import Dijkstra

ULazy.install(globals(), {
    'AlgoSPP': 'f_hs.algo.i_0_oospp.i_0_base:AlgoSPP',
    'SearchStateSPP': 'f_hs.algo.i_0_oospp.i_0_base:SearchStateSPP',
    'BFS': 'f_hs.algo.i_0_oospp.i_1_bfs:BFS',
    'AStar': 'f_hs.algo.i_0_oospp.i_1_astar:AStar',
    'AStarLookup': 'f_hs.algo.i_0_oospp.i_2_astar_lookup:AStarLookup',
    'AStarBPMX': 'f_hs.algo.i_0_oospp.i_3_astar_bpmx:AStarBPMX',
    'Dijkstra': 'f_hs.algo.i_0_oospp.i_2_dijkstra:Dijkstra',
})
