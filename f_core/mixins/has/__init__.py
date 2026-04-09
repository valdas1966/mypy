__all__ = [
    'HasKey',
    'HasName',
    'HasRowCol',
    'HasRowsCols',
]


def __getattr__(name: str):
    _lazy = {
        'HasKey': 'f_core.mixins.has.key',
        'HasName': 'f_core.mixins.has.name',
        'HasRowCol': 'f_core.mixins.has.row_col',
        'HasRowsCols': 'f_core.mixins.has.rows_cols',
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
