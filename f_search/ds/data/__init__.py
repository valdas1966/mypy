__all__ = [
    'HasDataState',
    'DataBestFirst',
    'DataHeuristics',
    'DataHeuristicsVector',
    'DataCached',
]


def __getattr__(name: str):
    _lazy = {
        'HasDataState': 'f_search.ds.data.mixins',
        'DataBestFirst': 'f_search.ds.data.i_0_best_first',
        'DataHeuristics': 'f_search.ds.data.i_1_heuristics',
        'DataHeuristicsVector': 'f_search.ds.data.i_2_heuristics_vector',
        'DataCached': 'f_search.ds.data.cached',
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
