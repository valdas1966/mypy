from typing import TYPE_CHECKING

from f_core.imports import ULazy

if TYPE_CHECKING:
    from f_hs.algo.i_1_mospp.i_1_astar_rep import AStarRepMOSPP
    from f_hs.algo.i_1_mospp.i_1_astar_flip import AStarFlipMOSPP
    from f_hs.algo.i_1_mospp.i_1_bfs_flip import BFSFlipMOSPP
    from f_hs.algo.i_1_mospp.i_1_dijkstra_flip import DijkstraFlipMOSPP

ULazy.install(globals(), {
    'AStarRepMOSPP': 'f_hs.algo.i_1_mospp.i_1_astar_rep:AStarRepMOSPP',
    'AStarFlipMOSPP':
        'f_hs.algo.i_1_mospp.i_1_astar_flip:AStarFlipMOSPP',
    'BFSFlipMOSPP': 'f_hs.algo.i_1_mospp.i_1_bfs_flip:BFSFlipMOSPP',
    'DijkstraFlipMOSPP': 'f_hs.algo.i_1_mospp.i_1_dijkstra_flip:DijkstraFlipMOSPP',
})
