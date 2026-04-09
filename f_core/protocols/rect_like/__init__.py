__all__ = ['RectLike']


def __getattr__(name: str):
    _lazy = {
        'RectLike': 'f_core.protocols.rect_like.main',
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
