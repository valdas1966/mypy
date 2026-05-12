__all__ = ['ExtendableMOSPP', 'is_extendable']


def __getattr__(name: str):
    _lazy = {
        'ExtendableMOSPP': 'f_hs.algo.i_1_mospp.mixins.extendable',
        'is_extendable': 'f_hs.algo.i_1_mospp.mixins.extendable',
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
