__all__ = [
    'setup_log',
    'get_log',
    'ColorLog',
    'log_func',
]


def __getattr__(name: str):
    _lazy = {
        'setup_log': 'f_log.u_log',
        'get_log': 'f_log.u_log',
        'ColorLog': 'f_log.color_log',
        'log_func': 'f_log.u_decorator',
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
