__all__ = ['KxAStarMOSPP']


def __getattr__(name: str):
    _lazy = {
        'KxAStarMOSPP': 'f_hs.algo.i_1_mospp.i_1_kxastar',
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
