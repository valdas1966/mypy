from f_graph.path_finding.algo import Algo, Problem, Path, Data, Ops
from f_ds.queues.i_1_fifo import QueueFIFO


class BFS(Algo):
    """
    ============================================================================
     BFS (Breadth-First-Search) Algorithm.
    ============================================================================
    """

    def __init__(self,
                 problem: Problem,
                 name: str = 'BFS') -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        data = Data(problem=problem, type_queue=QueueFIFO)
        ops = Ops(problem=problem, data=data)
        path = Path()
        Algo.__init__(self,
                      problem=problem,
                      data=data,
                      ops=ops,
                      path=path,
                      name=name)
