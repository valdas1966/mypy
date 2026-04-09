__all__ = [
    'AlgoSPP',
    'AStar',
    'BFS',
    'Dijkstra',
    'AStarReusable',
    'AStarCached',
]


def __getattr__(name: str):
    _lazy = {
        'AlgoSPP': 'f_search.algos.i_1_spp.i_0_base',
        'AStar': 'f_search.algos.i_1_spp.i_1_astar',
        'BFS': 'f_search.algos.i_1_spp.i_1_bfs',
        'Dijkstra': 'f_search.algos.i_1_spp.i_1_dijkstra',
        'AStarReusable': 'f_search.algos.i_1_spp.i_2_astar_reusable',
        'AStarCached': 'f_search.algos.i_1_spp.i_3_astar_cached',
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
