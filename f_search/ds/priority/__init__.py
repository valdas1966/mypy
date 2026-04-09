__all__ = [
    'PriorityKey',
    'PriorityG',
    'PriorityGH',
    'PriorityGHFlags',
]


def __getattr__(name: str):
    _lazy = {
        'PriorityKey': 'f_search.ds.priority.i_0_key.main',
        'PriorityG': 'f_search.ds.priority.i_1_g.main',
        'PriorityGH': 'f_search.ds.priority.i_2_gh.main',
        'PriorityGHFlags': 'f_search.ds.priority.i_3_gh_flags.main',
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
