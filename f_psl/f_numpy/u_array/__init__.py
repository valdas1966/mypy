__all__ = ['UArray']


def __getattr__(name: str):
    _lazy = {
        'UArray': 'f_psl.f_numpy.u_array.main',
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
