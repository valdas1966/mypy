from f_core.imports import ULazy

ULazy.install(globals(), {
    'KAStarInc': 'f_hs.algo.i_1_omspp.i_1_kastar_inc:KAStarInc',
    'KAStarAgg': 'f_hs.algo.i_1_omspp.i_1_kastar_agg:KAStarAgg',
    'KDijkstra': 'f_hs.algo.i_1_omspp.i_2_kdijkstra:KDijkstra',
    'KBFS': 'f_hs.algo.i_1_omspp.i_1_kbfs:KBFS',
    'KxAStarOMSPP': 'f_hs.algo.i_1_omspp.i_1_kxastar:KxAStarOMSPP',
})
