__all__ = ['UPdf', 'ResponsePdf']


def __getattr__(name: str):
    _lazy = {
        'UPdf': 'f_pdf.main',
        'ResponsePdf': 'f_pdf.response',
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
