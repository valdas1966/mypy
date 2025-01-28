from f_graph.path.one_to_one.heuristics import Heuristic, Node
from f_graph.path.one_to_one.problem import ProblemOneToOne


class GenHeuristic:
    """
    ============================================================================
     Generator of Heuristic-Functions.
    ============================================================================
    """

    @staticmethod
    def gen_manhattan(problem: ProblemOneToOne) -> Heuristic:
        """
        ========================================================================
         Generate a Manhattan-Distance Heuristic from a Node to a Goal.
        =======================================================================
        """
        distance = problem.graph.distance
        goal = problem.goal
        return Heuristic(lambda node: distance(node, goal), goal=goal)
