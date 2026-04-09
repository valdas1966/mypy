__all__ = ['HasGoal']


def __getattr__(name: str):
    _lazy = {
        'HasGoal': 'f_search.problems.mixins.has_goal.main',
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
