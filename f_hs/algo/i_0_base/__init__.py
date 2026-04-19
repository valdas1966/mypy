__all__ = ['AlgoSPP', 'SearchStateSPP']


def __getattr__(name: str):
    _lazy = {
        'AlgoSPP': 'f_hs.algo.i_0_base.main',
        'SearchStateSPP': 'f_hs.algo.i_0_base._search_state',
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
