from typing import TYPE_CHECKING

from f_core.imports import ULazy

if TYPE_CHECKING:
    from f_hs.algo.i_1_omspp.i_1_kastar_inc import KAStarInc
    from f_hs.algo.i_1_omspp.i_1_kastar_agg import KAStarAgg
    from f_hs.algo.i_1_omspp.i_2_kdijkstra import KDijkstra
    from f_hs.algo.i_1_omspp.i_1_kbfs import KBFS
    from f_hs.algo.i_1_omspp.i_1_kxastar import KxAStarOMSPP

ULazy.install(globals(), {
    'KAStarInc': 'f_hs.algo.i_1_omspp.i_1_kastar_inc:KAStarInc',
    'KAStarAgg': 'f_hs.algo.i_1_omspp.i_1_kastar_agg:KAStarAgg',
    'KDijkstra': 'f_hs.algo.i_1_omspp.i_2_kdijkstra:KDijkstra',
    'KBFS': 'f_hs.algo.i_1_omspp.i_1_kbfs:KBFS',
    'KxAStarOMSPP': 'f_hs.algo.i_1_omspp.i_1_kxastar:KxAStarOMSPP',
})
