__all__ = ['u_dir', 'u_txt', 'u_pathlib']


def __getattr__(name: str):
    _lazy_mod = {
        'u_dir': 'f_psl.os.u_dir',
        'u_txt': 'f_psl.file.u_txt',
        'u_pathlib': 'f_psl.pathlib.u_pathlib',
    }
    if name in _lazy_mod:
        from importlib import import_module
        mod = import_module(_lazy_mod[name])
        globals()[name] = mod
        return mod
    raise AttributeError(
        f"module {__name__!r} has no attribute {name!r}"
    )
