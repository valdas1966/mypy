from f_graph.path.generators.g_cache import GenCache
from f_graph.path.generators.g_boundary import GenBoundary, Boundary
from f_graph.path.generators.g_heuristic import GenHeuristic
from f_graph.path.algos.one_to_one.generators.g_problem import GenProblemOneToOne
from f_graph.path.algos.one_to_one.generators.g_state import GenStateOneToOne
from f_graph.path.algos.one_to_one.ops import OpsOneToOne


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
         Generate a 3x3 Ops with Explored-Cache.
        ========================================================================
        """
        problem = GenProblemOneToOne.gen_3x3()
        state = GenStateOneToOne.gen_priority()
        cache = GenCache.from_explored()
        boundary = Boundary()
        heuristic = GenHeuristic.gen_manhattan(graph=problem.graph,
                                               goal=problem.goal)
        ops = OpsOneToOne(problem=problem,
                          state=state,
                          cache=cache,
                          boundary=boundary,
                          heuristic=heuristic)
        return ops
    
    @staticmethod
    def first_row_branch_3x3_path() -> OpsOneToOne:
        """
        ========================================================================
         Generate a 3x3 Ops with Path-Cache.
        ========================================================================
        """
        problem = GenProblemOneToOne.gen_3x3()
        state = GenStateOneToOne.gen_priority()
        cache = GenCache.from_path()
        boundary = Boundary()
        heuristic = GenHeuristic.gen_manhattan(graph=problem.graph,
                                               goal=problem.goal)
        ops = OpsOneToOne(problem=problem,
                          state=state,
                          cache=cache,
                          boundary=boundary,
                          heuristic=heuristic)
        return ops
    
    @staticmethod
    def boundary_4x4() -> OpsOneToOne:
        """
        ========================================================================
         Generate a 4x4 Ops with Boundary.
        ========================================================================
        """
        problem = GenProblemOneToOne.boundary_4x4()
        state = GenStateOneToOne.gen_priority()
        cache = GenCache.boundary_4x4()
        boundary = GenBoundary.boundary_4x4()
        heuristic = GenHeuristic.gen_manhattan(graph=problem.graph, goal=problem.goal)
        return OpsOneToOne(problem=problem,
                           state=state,
                           cache=cache,
                           boundary=boundary,
                           heuristic=heuristic)
