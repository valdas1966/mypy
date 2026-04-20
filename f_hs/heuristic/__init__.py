__all__ = ['HBase', 'HCallable', 'HCached', 'HBounded', 'CacheEntry']


def __getattr__(name: str):
    _lazy = {
        'HBase':      'f_hs.heuristic.i_0_base',
        'CacheEntry': 'f_hs.heuristic.i_0_base',
        'HCallable':  'f_hs.heuristic.i_1_callable',
        'HCached':    'f_hs.heuristic.i_1_cached',
        'HBounded':   'f_hs.heuristic.i_1_bounded',
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
