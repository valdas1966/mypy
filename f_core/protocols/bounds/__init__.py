__all__ = ['SupportsBounds']


def __getattr__(name: str):
    _lazy = {
        'SupportsBounds': 'f_core.protocols.bounds.main',
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
