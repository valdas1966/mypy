__all__ = ['ProblemSPP', 'ProblemGrid']


def __getattr__(name: str):
    _lazy = {
        'ProblemSPP': 'f_hs.problem.i_0_base',
        'ProblemGrid': 'f_hs.problem.i_1_grid',
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
