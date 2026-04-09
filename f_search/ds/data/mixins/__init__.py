__all__ = ['HasDataState']


def __getattr__(name: str):
    _lazy = {
        'HasDataState': 'f_search.ds.data.mixins.has_data_state',
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
