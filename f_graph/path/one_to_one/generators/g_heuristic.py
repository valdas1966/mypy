from f_graph.path.one_to_one.heuristics import Heuristic
from f_graph.path.graph import GraphPath as Graph, Node


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
        =======================================================================
        """
        distance = graph.distance
        return Heuristic(lambda node, goal: distance(node, goal), goal=goal)

    @staticmethod
    def gen_none() -> Heuristic:
        """
        ========================================================================
         Generate a None-Heuristic.
        ========================================================================
        """
        return Heuristic(lambda node, goal: None, None)
