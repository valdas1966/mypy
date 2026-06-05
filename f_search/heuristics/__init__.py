from typing import TYPE_CHECKING

from f_core.imports import ULazy

if TYPE_CHECKING:
    from f_search.heuristics.protocol import HeuristicsProtocol
    from f_search.heuristics.manhattan import HeuristicsManhattan
    from f_search.heuristics.aggregative import HeuristicsAggregative
    from f_search.heuristics.phi import UPhi
    from f_search.heuristics.phi import PhiFunc

ULazy.install(globals(), {
    'HeuristicsProtocol': 'f_search.heuristics.protocol:HeuristicsProtocol',
    'HeuristicsManhattan': 'f_search.heuristics.manhattan:HeuristicsManhattan',
    'HeuristicsAggregative': 'f_search.heuristics.aggregative:HeuristicsAggregative',
    'UPhi': 'f_search.heuristics.phi:UPhi',
    'PhiFunc': 'f_search.heuristics.phi:PhiFunc',
})
