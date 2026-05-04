__all__ = [
    'AlgoSPP',
    'SearchStateSPP',
    'BFS',
    'AStar',
    'AStarLookup',
    'AStarBPMX',
    'AStarLookupBPMX',
    'Dijkstra',
]


def __getattr__(name: str):
    _lazy = {
        'AlgoSPP': 'f_hs.algo.i_0_oospp.i_0_base',
        'SearchStateSPP': 'f_hs.algo.i_0_oospp.i_0_base',
        'BFS': 'f_hs.algo.i_0_oospp.i_1_bfs',
        'AStar': 'f_hs.algo.i_0_oospp.i_1_astar',
        'AStarLookup': 'f_hs.algo.i_0_oospp.i_2_astar_lookup',
        'AStarBPMX': 'f_hs.algo.i_0_oospp.i_2_astar_bpmx',
        'AStarLookupBPMX': 'f_hs.algo.i_0_oospp.i_3_astar_lookup_bpmx',
        'Dijkstra': 'f_hs.algo.i_0_oospp.i_2_dijkstra',
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
