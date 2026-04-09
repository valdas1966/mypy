__all__ = [
    'AlgoOMSPP',
    'AStarRepeated',
    'AStarRepeatedBackward',
    'AStarAggregative',
    'BFSIncremental',
    'AStarIncremental',
    'DijkstraIncremental',
    'AStarIncrementalBackward',
]


def __getattr__(name: str):
    _lazy = {
        'AlgoOMSPP': 'f_search.algos.i_2_omspp.i_0_base',
        'AStarRepeated': 'f_search.algos.i_2_omspp.i_1_repeated.astar',
        'AStarRepeatedBackward': 'f_search.algos.i_2_omspp.i_1_repeated.astar_backward',
        'AStarAggregative': 'f_search.algos.i_2_omspp.i_1_aggregative',
        'BFSIncremental': 'f_search.algos.i_2_omspp.i_1_incremental.bfs',
        'AStarIncremental': 'f_search.algos.i_2_omspp.i_1_incremental.astar',
        'DijkstraIncremental': 'f_search.algos.i_2_omspp.i_1_incremental.dijkstra',
        'AStarIncrementalBackward': 'f_search.algos.i_2_omspp.i_1_incremental.astar_backward',
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
