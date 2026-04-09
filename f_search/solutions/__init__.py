__all__ = [
    'SolutionSearch',
    'SolutionSPP',
    'SolutionOMSPP',
    'SolutionNeighborhood',
]


def __getattr__(name: str):
    _lazy = {
        'SolutionSearch': 'f_search.solutions.i_0_base',
        'SolutionSPP': 'f_search.solutions.i_1_spp',
        'SolutionOMSPP': 'f_search.solutions.i_2_omspp',
        'SolutionNeighborhood': 'f_search.solutions.i_1_neighborhood',
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
