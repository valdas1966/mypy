from f_graph.path.one_to_one.state import State
from f_ds.queues.i_1_priority import QueuePriority


class GenState:
    """
    ============================================================================
     State-Generator for One-To-One Path-Finding Problems.
    ============================================================================
    """

    @staticmethod
    def gen_with_priority() -> State:
        """
        ========================================================================
         Generate an empty state with a priority queue.
        ========================================================================
        """
        return State(type_queue=QueuePriority)
