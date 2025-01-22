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
        node_0_1 = problem.graph[0, 1]
        node_0_1.parent = start
        node_0_2 = problem.graph[0, 2]
        node_0_2.parent = node_0_1
        best = problem.graph[1, 2]
        best.parent = node_0_2
        state = StateOneToOne(type_queue=QueuePriority)
        state.best = best
        return state
