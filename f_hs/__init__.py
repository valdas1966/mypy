__all__ = [
    'StateBase',
    'StateCell',
    'ProblemSPP',
    'ProblemGrid',
    'SolutionSPP',
    'AlgoSPP',
    'BFS',
    'AStar',
    'Dijkstra',
]


def __getattr__(name: str):
    _lazy = {
        'StateBase': 'f_hs.state',
        'StateCell': 'f_hs.state',
        'ProblemSPP': 'f_hs.problem',
        'ProblemGrid': 'f_hs.problem',
        'SolutionSPP': 'f_hs.solution',
        'AlgoSPP': 'f_hs.algo',
        'BFS': 'f_hs.algo',
        'AStar': 'f_hs.algo',
        'Dijkstra': 'f_hs.algo',
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
