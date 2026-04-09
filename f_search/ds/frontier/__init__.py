__all__ = ['FrontierBase', 'FrontierFifo', 'FrontierPriority']


def __getattr__(name: str):
    _lazy = {
        'FrontierBase': 'f_search.ds.frontier.i_0_base',
        'FrontierFifo': 'f_search.ds.frontier.i_1_fifo',
        'FrontierPriority': 'f_search.ds.frontier.i_1_priority',
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
