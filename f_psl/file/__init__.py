__all__ = ['u_txt']


def __getattr__(name: str):
    if name == 'u_txt':
        from importlib import import_module
        mod = import_module('f_psl.file.u_txt')
        globals()['u_txt'] = mod
        return mod
    raise AttributeError(
        f"module {__name__!r} has no attribute {name!r}"
    )
