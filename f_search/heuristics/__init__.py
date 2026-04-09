__all__ = [
    'HeuristicsProtocol',
    'HeuristicsManhattan',
    'HeuristicsAggregative',
    'UPhi',
    'PhiFunc',
]


def __getattr__(name: str):
    _lazy = {
        'HeuristicsProtocol': 'f_search.heuristics.protocol',
        'HeuristicsManhattan': 'f_search.heuristics.manhattan',
        'HeuristicsAggregative': 'f_search.heuristics.aggregative',
        'UPhi': 'f_search.heuristics.phi',
        'PhiFunc': 'f_search.heuristics.phi',
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
