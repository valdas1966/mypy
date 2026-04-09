__all__ = ['UDateTime']


def __getattr__(name: str):
    _lazy = {
        'UDateTime': 'f_psl.datetime.main',
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
