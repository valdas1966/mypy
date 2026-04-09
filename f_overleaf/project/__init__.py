__all__ = ['ProjectOverLeaf']


def __getattr__(name: str):
    _lazy = {
        'ProjectOverLeaf': 'f_overleaf.project.main',
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
