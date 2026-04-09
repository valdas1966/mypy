__all__ = ['GridBase', 'GridMap', 'CellMap']


def __getattr__(name: str):
    _lazy = {
        'GridBase': 'f_ds.grids.grid',
        'GridMap': 'f_ds.grids.grid',
        'CellMap': 'f_ds.grids.cell',
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
