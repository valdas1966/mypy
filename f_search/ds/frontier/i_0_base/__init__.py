__all__ = ['FrontierBase']


def __getattr__(name: str):
    _lazy = {
        'FrontierBase': 'f_search.ds.frontier.i_0_base.main',
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
