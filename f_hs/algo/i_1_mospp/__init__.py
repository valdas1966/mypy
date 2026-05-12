__all__ = ['KxAStarMOSPP', 'KBFSMOSPP', 'KDijkstraMOSPP']


def __getattr__(name: str):
    _lazy = {
        'KxAStarMOSPP': 'f_hs.algo.i_1_mospp.i_1_kxastar',
        'KBFSMOSPP': 'f_hs.algo.i_1_mospp.i_1_kbfs',
        'KDijkstraMOSPP': 'f_hs.algo.i_1_mospp.i_1_kdijkstra',
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
