__all__ = [
    '_Nav',
    '_Folders',
    '_Download',
    '_Upload',
    '_Read',
    '_ReadResponse',
]


def __getattr__(name: str):
    _lazy = {
        '_Nav': 'f_google.services.drive._internal._nav',
        '_Folders': 'f_google.services.drive._internal._folders',
        '_Download': 'f_google.services.drive._internal._download',
        '_Upload': 'f_google.services.drive._internal._upload',
        '_Read': 'f_google.services.drive._internal._read',
        '_ReadResponse': 'f_google.services.drive._internal._read_response',
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
