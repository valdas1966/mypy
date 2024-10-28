from f_ai.hs.algos.one_to_one.a_star import AStar, Problem
from f_ai.hs.nodes.i_1_f_cell import NodeFCell as Node
from functools import partial


class UAlgos:
    """
    ============================================================================
     Utils-Class for generating One-to-One heuristic Path-Algorithms.
    ============================================================================
    """

    @staticmethod
    def astar(problem: Problem) -> AStar:
        """
        ========================================================================
         Run AStar with the given problem.
        ========================================================================
        """
        heuristics = partial(problem.graph.distance, node_b=problem.goal)
        return AStar[Problem, Node](problem=problem, heuristics=heuristics)
