__all__ = ['u_iter']


def __getattr__(name: str):
    if name == 'u_iter':
        from importlib import import_module
        mod = import_module('f_utils.iter.u_iter')
        globals()['u_iter'] = mod
        return mod
    raise AttributeError(
        f"module {__name__!r} has no attribute {name!r}"
    )
