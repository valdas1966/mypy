__all__ = [
    'HasStart',
    'HasStarts',
    'HasGoal',
    'HasGoals',
]


def __getattr__(name: str):
    _lazy = {
        'HasStart': 'f_search.problems.mixins.has_start',
        'HasStarts': 'f_search.problems.mixins.has_starts',
        'HasGoal': 'f_search.problems.mixins.has_goal',
        'HasGoals': 'f_search.problems.mixins.has_goals',
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
