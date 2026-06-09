from typing import TYPE_CHECKING

from f_core.imports import ULazy

if TYPE_CHECKING:
    from f_hs.algo.i_1_mospp.i_1_astar_rep import AStarRepMOSPP
    from f_hs.algo.i_1_mospp.i_1_kastar_inc import KAStarIncMOSPP
    from f_hs.algo.i_1_mospp.i_1_kbfs import KBFSMOSPP
    from f_hs.algo.i_1_mospp.i_1_kdijkstra import KDijkstraMOSPP

ULazy.install(globals(), {
    'AStarRepMOSPP': 'f_hs.algo.i_1_mospp.i_1_astar_rep:AStarRepMOSPP',
    'KAStarIncMOSPP':
        'f_hs.algo.i_1_mospp.i_1_kastar_inc:KAStarIncMOSPP',
    'KBFSMOSPP': 'f_hs.algo.i_1_mospp.i_1_kbfs:KBFSMOSPP',
    'KDijkstraMOSPP': 'f_hs.algo.i_1_mospp.i_1_kdijkstra:KDijkstraMOSPP',
})
