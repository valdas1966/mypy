__all__ = ['KAStarInc', 'KAStarAgg', 'KDijkstra', 'KBFS',
           'KxAStarOMSPP']


def __getattr__(name: str):
    _lazy = {
        'KAStarInc': 'f_hs.algo.i_1_omspp.i_1_kastar_inc',
        'KAStarAgg': 'f_hs.algo.i_1_omspp.i_1_kastar_agg',
        'KDijkstra': 'f_hs.algo.i_1_omspp.i_2_kdijkstra',
        'KBFS': 'f_hs.algo.i_1_omspp.i_1_kbfs',
        'KxAStarOMSPP': 'f_hs.algo.i_1_omspp.i_1_kxastar',
    }
    if name in _lazy:
        from importlib import import_module
        mod = import_module(_lazy[name])
        val = getattr(mod, name)
        globals()[name] = val
        return val
    raise AttributeError(
        f"module {__name__!r} has no attribute {name!r}"
    )
