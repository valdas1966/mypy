from f_graph.path.one_to_one.generators.g_problem import GenProblemOneToOne, Node
from typing import Callable


class GenCache:
    """
    ============================================================================
     Cache-Generator for One-to-One Path-Finding Problems.
    ============================================================================
    """

    @staticmethod
    def gen_3x3() -> dict[Node, Callable[[], list[Node]]]:
        """
        ========================================================================
         Generate a cache for a 3x3 problem.
        ========================================================================
        """
        cache: dict[Node, Callable[[], list[Node]]] = dict()
        problem = GenProblemOneToOne.gen_3x3()
        goal, pre_goal = problem.goal, problem.pre_goal
        cache[goal] = lambda: []
        cache[pre_goal] = lambda: [goal]
        return cache
