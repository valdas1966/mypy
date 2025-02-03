from f_graph.path.heuristic import Heuristic, TypeHeuristic
from f_graph.path.graph import GraphPath as Graph, NodePath as Node


class GenHeuristic:
    """
    ============================================================================
     Generator of Heuristic-Functions.
    ============================================================================
    """

    @staticmethod
    def gen_manhattan(graph: Graph, goal: Node) -> Heuristic:
        """
        ========================================================================
         Generate a Manhattan-Distance Heuristic from a Node to a Goal.
        ========================================================================
        """
        return Heuristic(graph=graph,
                         goal=goal,
                         type_heuristic=TypeHeuristic.MANHATTAN)

    @staticmethod
    def gen_zero(graph: Graph, goal: Node) -> Heuristic:
        """
        ========================================================================
         Generate a Zero-Heuristic to every Node.
        ========================================================================
        """
        return Heuristic(graph=graph,
                         goal=goal,
                         type_heuristic=TypeHeuristic.ZERO)
