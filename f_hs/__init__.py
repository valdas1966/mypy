__all__ = [
    'StateBase',
    'StateCell',
    'ProblemSPP',
    'ProblemGrid',
    'SolutionSPP',
    'SolutionOMSPP',
    'SolutionMOSPP',
    'SolutionPerKey',
    'AlgoSPP',
    'BFS',
    'AStar',
    'AStarLookup',
    'Dijkstra',
    'KAStarInc',
    'KAStarAgg',
    'KBFS',
    'KDijkstra',
    'HBase',
    'HCallable',
    'HCached',
    'HBounded',
    'CacheEntry',
]


def __getattr__(name: str):
    _lazy = {
        'StateBase': 'f_hs.state',
        'StateCell': 'f_hs.state',
        'ProblemSPP': 'f_hs.problem',
        'ProblemGrid': 'f_hs.problem',
        'SolutionSPP': 'f_hs.solution',
        'SolutionOMSPP': 'f_hs.solution',
        'SolutionMOSPP': 'f_hs.solution',
        'SolutionPerKey': 'f_hs.solution',
        'AlgoSPP': 'f_hs.algo',
        'BFS': 'f_hs.algo',
        'AStar': 'f_hs.algo',
        'AStarLookup': 'f_hs.algo',
        'Dijkstra': 'f_hs.algo',
        'KAStarInc':  'f_hs.algo.i_1_omspp',
        'KAStarAgg':  'f_hs.algo.i_1_omspp',
        'KBFS':       'f_hs.algo.i_1_omspp',
        'KDijkstra':  'f_hs.algo.i_1_omspp',
        'HBase':      'f_hs.heuristic',
        'HCallable':  'f_hs.heuristic',
        'HCached':    'f_hs.heuristic',
        'HBounded':   'f_hs.heuristic',
        'CacheEntry': 'f_hs.heuristic',
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
