__all__ = ['ExtendableOMSPP', 'is_extendable']


def __getattr__(name: str):
    _lazy = {
        'ExtendableOMSPP': 'f_hs.algo.i_1_omspp.mixins.extendable',
        'is_extendable': 'f_hs.algo.i_1_omspp.mixins.extendable',
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
