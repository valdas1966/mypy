from typing import TYPE_CHECKING

from f_core.imports import ULazy

if TYPE_CHECKING:
    from f_hs.state import StateBase
    from f_hs.state import StateCell
    from f_hs.problem import ProblemSPP
    from f_hs.problem import ProblemGrid
    from f_hs.solution import SolutionSPP
    from f_hs.solution import SolutionOMSPP
    from f_hs.solution import SolutionMOSPP
    from f_hs.solution import SolutionPerKey
    from f_hs.algo import AlgoSPP
    from f_hs.algo import BFS
    from f_hs.algo import AStar
    from f_hs.algo import AStarLookup
    from f_hs.algo import AStarBPMX
    from f_hs.algo import Dijkstra
    from f_hs.algo.i_1_omspp import KAStarInc
    from f_hs.algo.i_1_omspp import KAStarAgg
    from f_hs.algo.i_1_omspp import KBFS
    from f_hs.algo.i_1_omspp import KDijkstra
    from f_hs.heuristic import HBase
    from f_hs.heuristic import HCallable
    from f_hs.heuristic import HCached
    from f_hs.heuristic import HBounded
    from f_hs.heuristic import CacheEntry

ULazy.install(globals(), {
    'StateBase': 'f_hs.state:StateBase',
    'StateCell': 'f_hs.state:StateCell',
    'ProblemSPP': 'f_hs.problem:ProblemSPP',
    'ProblemGrid': 'f_hs.problem:ProblemGrid',
    'SolutionSPP': 'f_hs.solution:SolutionSPP',
    'SolutionOMSPP': 'f_hs.solution:SolutionOMSPP',
    'SolutionMOSPP': 'f_hs.solution:SolutionMOSPP',
    'SolutionPerKey': 'f_hs.solution:SolutionPerKey',
    'AlgoSPP': 'f_hs.algo:AlgoSPP',
    'BFS': 'f_hs.algo:BFS',
    'AStar': 'f_hs.algo:AStar',
    'AStarLookup': 'f_hs.algo:AStarLookup',
    'AStarBPMX': 'f_hs.algo:AStarBPMX',
    'Dijkstra': 'f_hs.algo:Dijkstra',
    'KAStarInc': 'f_hs.algo.i_1_omspp:KAStarInc',
    'KAStarAgg': 'f_hs.algo.i_1_omspp:KAStarAgg',
    'KBFS': 'f_hs.algo.i_1_omspp:KBFS',
    'KDijkstra': 'f_hs.algo.i_1_omspp:KDijkstra',
    'HBase': 'f_hs.heuristic:HBase',
    'HCallable': 'f_hs.heuristic:HCallable',
    'HCached': 'f_hs.heuristic:HCached',
    'HBounded': 'f_hs.heuristic:HBounded',
    'CacheEntry': 'f_hs.heuristic:CacheEntry',
})
