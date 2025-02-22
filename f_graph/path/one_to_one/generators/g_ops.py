from f_graph.path.generators.g_cache import GenCache
from f_graph.path.generators.g_boundary import GenBoundary
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
    def first_row_branch_3x3_explored() -> OpsOneToOne:
        """
        ========================================================================
         Generate a 3x3 Ops with Explored Cache.
        ========================================================================
        """
        problem = GenProblemOneToOne.gen_3x3()
