__all__ = [
    'FrontierBase',
    'FrontierFIFO',
    'FrontierPriority',
]


def __getattr__(name: str):
    _lazy = {
        'FrontierBase': 'f_hs.frontier.i_0_base',
        'FrontierFIFO': 'f_hs.frontier.i_1_fifo',
        'FrontierPriority': 'f_hs.frontier.i_1_priority',
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
