from f_heuristic_search.algos.spp.a_star.i_0_base import AStar
from f_heuristic_search.problem_types.spp import SPP
from f_heuristic_search.algos.strategy.heuristic.manual import HeuristicManual
from f_heuristic_search.algos.spp.strategy.termination.i_1_goal import TerminationGoal


class AStarManual(AStar):
    """
    ============================================================================
     AStar with Manual-Heuristics.
    ============================================================================
    """

    def __init__(self, spp: SPP) -> None:
        """
        ========================================================================
         Init Private Attributes.
        ========================================================================
        """
        heuristic = HeuristicManual(heuristics=spp.heuristics)
        termination = TerminationGoal(goal=spp.goal)
        AStar.__init__(self, spp, heuristic, termination)

