__all__ = ['AStarRepeated', 'AStarRepeatedBackward']


def __getattr__(name: str):
    _lazy = {
        'AStarRepeated': 'f_search.algos.i_2_omspp.i_1_repeated.astar',
        'AStarRepeatedBackward': 'f_search.algos.i_2_omspp.i_1_repeated.astar_backward',
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
