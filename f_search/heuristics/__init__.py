from f_core.imports import ULazy

ULazy.install(globals(), {
    'HeuristicsProtocol': 'f_search.heuristics.protocol:HeuristicsProtocol',
    'HeuristicsManhattan': 'f_search.heuristics.manhattan:HeuristicsManhattan',
    'HeuristicsAggregative': 'f_search.heuristics.aggregative:HeuristicsAggregative',
    'UPhi': 'f_search.heuristics.phi:UPhi',
    'PhiFunc': 'f_search.heuristics.phi:PhiFunc',
})
