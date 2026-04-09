__all__ = ['Spread', 'Sheet', 'Cell']


def __getattr__(name: str):
    _lazy = {
        'Spread': 'f_google.services.sheets.spread',
        'Sheet': 'f_google.services.sheets.sheet',
        'Cell': 'f_google.services.sheets.cell',
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
