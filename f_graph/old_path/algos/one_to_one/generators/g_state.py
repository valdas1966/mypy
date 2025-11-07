from f_graph.old_path.algos.one_to_one.state import StateOneToOne, TypeQueue
from f_graph.old_path.algos.one_to_one.generators.g_problem import GenProblemOneToOne


class GenStateOneToOne:
    """
    ============================================================================
     Generator of StateOneToOne.
    ============================================================================
    """

    @staticmethod
    def gen_priority() -> StateOneToOne:
        """
        ========================================================================
         Generate a State with a generated list as a Priority-Queue.
        ========================================================================
        """
        type_queue = TypeQueue.PRIORITY
        state = StateOneToOne(type_queue=type_queue)
        problem = GenProblemOneToOne.gen_3x3()
        graph = problem.graph
        graph[0, 1].parent = graph[0, 0]
        graph[1, 0].parent = graph[0, 0]
        state.explored.add(graph[0, 0])
        state.generated.push(item=graph[1, 0])
        state.best = graph[0, 1]
        return state

    @staticmethod
    def gen_fifo() -> StateOneToOne:
        """
        ========================================================================
         Generate a State with a generated list as a FIFO-Queue.
        ========================================================================
        """
        type_queue = TypeQueue.FIFO
        return StateOneToOne(type_queue=type_queue)