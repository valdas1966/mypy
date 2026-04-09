__all__ = [
    'ProblemSearch',
    'ProblemSPP',
    'ProblemOMSPP',
    'ProblemMMSPP',
    'ProblemNeighborhood',
]


def __getattr__(name: str):
    _lazy = {
        'ProblemSearch': 'f_search.problems.i_0_base',
        'ProblemSPP': 'f_search.problems.i_1_spp',
        'ProblemOMSPP': 'f_search.problems.i_2_omspp',
        'ProblemMMSPP': 'f_search.problems.i_3_mmspp',
        'ProblemNeighborhood': 'f_search.problems.i_1_neighborhood',
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
