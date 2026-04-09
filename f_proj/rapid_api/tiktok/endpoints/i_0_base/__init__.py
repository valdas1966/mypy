__all__ = ['Endpoint']


def __getattr__(name: str):
    _lazy = {
        'Endpoint': '.main',
    }
    if name in _lazy:
        from importlib import import_module
        mod = import_module(_lazy[name], __package__)
        val = getattr(mod, name)
        globals()[name] = val
        return val
    raise AttributeError(
        f"module {__name__!r} has no attribute {name!r}"
    )
