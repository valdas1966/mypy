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
        problem = GenProblemOneToOne.gen_3x3()
        cache: dict[Node, Callable[[], list[Node]]] = dict()
        goal = problem.graph[0, 2]
        best = problem.graph[0, 1]
        cache[goal] = lambda: []
        cache[best] = lambda: [goal]
        return cache
