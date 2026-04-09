__all__ = ['ProcessIO', 'ProcessParallel']


def __getattr__(name: str):
    _lazy = {
        'ProcessIO': 'f_core.processes.i_2_io',
        'ProcessParallel': 'f_core.processes.i_3_parallel',
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
