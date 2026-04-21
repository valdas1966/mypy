__all__ = ['Cluster', 'ClusterDiamond', 'PairCluster']


def __getattr__(name: str):
    _lazy = {
        'Cluster': '.i_0_base',
        'ClusterDiamond': '.i_1_diamond',
        'PairCluster': '.pair',
    }
    if name in _lazy:
        from importlib import import_module
        mod = import_module(_lazy[name], __package__)
        val = getattr(mod, name)
        globals()[name] = val
        return val
    raise AttributeError(
        f"module {__name__!r} has no attribute {name!r}"
    )
