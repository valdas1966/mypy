from f_hs.algos.a_star import AStar, ProblemOneToOne
from f_hs.nodes.i_1_f_cell import NodeFCell
from f_hs.heuristics.i_1_manhattan import HeuristicsManhattan
from typing import TypeVar

Problem = TypeVar('Problem', bound=ProblemOneToOne)
Node = TypeVar('Node', bound=NodeFCell)


class AStarGrid(AStar[ProblemOneToOne, NodeFCell]):
    """
    ============================================================================
     AStar Algo for Grids.
    ============================================================================
    """

    def __init__(self, problem: ProblemOneToOne) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        heuristics = HeuristicsManhattan(problem=problem).eval
        AStar.__init__(self, problem=problem, heuristics=heuristics)
