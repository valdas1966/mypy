from f_graph.path.generators.g_cache import GenCache
from f_graph.path.generators.g_heuristic import GenHeuristic
from f_graph.path.one_to_one.generators.g_problem import GenProblemOneToOne
from f_graph.path.one_to_one.generators.g_state import GenStateOneToOne
from f_graph.path.one_to_one.ops import OpsOneToOne


class GenOps:
    """
    ============================================================================
     Ops Generator.
    ============================================================================
    """

    @staticmethod
    def gen_3x3() -> OpsOneToOne:
        """
        ========================================================================
         Generate a 3x3 Ops.
        ========================================================================
        """
        problem = GenProblemOneToOne.gen_3x3()
        state = GenStateOneToOne.gen_priority()
        cache = GenCache.gen_3x3()
        heuristic = GenHeuristic.gen_zero(graph=problem.graph,
                                          goal=problem.goal)
        return OpsOneToOne(problem=problem,
                           state=state,
                           cache=cache,
                           heuristic=heuristic)
