from f_hs.heuristics.i_0_base import HeuristicsBase, ProblemPath
from f_hs.nodes.i_1_f_cell import NodeFCell
from typing import TypeVar

Node = TypeVar('Node', bound=NodeFCell)
Problem = TypeVar('Problem', bound=ProblemPath)


class HeuristicsManhattan(HeuristicsBase[Node, Problem]):
    """
    ============================================================================
     Heuristics represented Manhattan-Distance between Node and Goal.
    ============================================================================
    """

    def eval(self, node: Node) -> int:
        """
        ========================================================================
         Return Manhattan-Distance from Node to Goal.
        ========================================================================
        """
        distance = self._problem.graph.distance
        return distance(node, self._problem.goal)