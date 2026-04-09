__all__ = ['StateBase', 'StateCell']


def __getattr__(name: str):
    _lazy = {
        'StateBase': 'f_hs.state.i_0_base',
        'StateCell': 'f_hs.state.i_1_cell',
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
