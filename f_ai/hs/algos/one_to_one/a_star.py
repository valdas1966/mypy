from f_graph.algos.one_to_one.i_1_core import AlgoOneToOneCore, Problem
from f_ds.old_queues.i_1_priority import QueuePriority
from f_ai.hs.ops.node import OpsNodeHS, Node
from typing import Callable


class AStar(AlgoOneToOneCore[Problem, Node]):
    """
    ============================================================================
     A* Algorithm.
    ============================================================================
    """

    def __init__(self,
                 problem: Problem,
                 heuristics: Callable[[Node], int],
                 name: str = 'AStar') -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        self._heuristics = heuristics
        AlgoOneToOneCore.__init__(self,
                                  problem=problem,
                                  type_queue=QueuePriority,
                                  name=name)

    def _create_ops_node(self) -> OpsNodeHS[Problem, Node]:
        """
        ========================================================================
         Dependency Injection - Create Operations-on-Node object.
        ========================================================================
        """
        return OpsNodeHS(problem=self._problem,
                         data=self._data,
                         heuristics=self._heuristics)
