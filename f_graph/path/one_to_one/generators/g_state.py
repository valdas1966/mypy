from f_graph.path.one_to_one.state import StateOneToOne
from f_graph.path.one_to_one.generators.g_problem import GenProblemOneToOne
from f_ds.queues.i_1_priority import QueuePriority


class GenStateOneToOne:
    """
    ============================================================================
     State-Generator for One-To-One Path-Finding Problems.
    ============================================================================
    """

    @staticmethod
    def gen_3x3() -> StateOneToOne:
        """
        ========================================================================
         Generate a state for a 3x3 problem.
        ========================================================================
        """
        problem = GenProblemOneToOne.gen_3x3()
        start = problem.graph[0, 0]
        best = problem.graph[0, 1]
        best.parent = start
        state = StateOneToOne(type_queue=QueuePriority)
        state.best = best
        return state
