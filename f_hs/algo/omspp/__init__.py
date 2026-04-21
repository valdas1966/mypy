__all__ = ['KAStarInc', 'KAStarAgg']


def __getattr__(name: str):
    _lazy = {
        'KAStarInc': 'f_hs.algo.omspp.i_1_kastar_inc',
        'KAStarAgg': 'f_hs.algo.omspp.i_1_kastar_agg',
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
