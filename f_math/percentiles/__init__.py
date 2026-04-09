__all__ = ['UPercentiles', 'Bin']


def __getattr__(name: str):
    _lazy = {
        'UPercentiles': 'f_math.percentiles.utils',
        'Bin': 'f_math.percentiles.bin',
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
