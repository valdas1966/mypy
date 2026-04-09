__all__ = ['GridBase', 'GridMap']


def __getattr__(name: str):
    _lazy = {
        'GridBase': 'f_ds.grids.grid.base',
        'GridMap': 'f_ds.grids.grid.map',
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
