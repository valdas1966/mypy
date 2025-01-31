from f_graph.path.generators.g_problem import GenProblemPath
from f_graph.path.generators.g_state import GenState
from f_graph.path.generators.g_cache import GenCache
from f_graph.path.generators.g_heuristic import GenHeuristic    
from f_graph.path.ops import Ops


class GenOps:
    """
    ============================================================================
     Ops Generator.
    ============================================================================
    """

    @staticmethod
    def gen_3x3() -> Ops:
        """
        ========================================================================
         Generate a 3x3 Ops.
        ========================================================================
        """
        problem = GenProblemPath.gen_3x3()
        state = GenState.gen_3x3()
        cache = GenCache.gen_3x3()
        heuristic = GenHeuristic.gen_none()
        return Ops(problem=problem,
                   state=state,
                   cache=cache,
                   heuristic=heuristic)
