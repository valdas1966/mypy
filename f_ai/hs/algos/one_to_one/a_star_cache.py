from f_graph.algos.one_to_one.i_1_cache import AlgoOneToOneCache, Problem, Cache
from f_ds.queues.i_1_priority import QueuePriority
from f_ai.hs.ops.node import OpsNodeHS, Node
from typing import Callable


class AStarCache(AlgoOneToOneCache[Problem, Node]):
    """
    ============================================================================
     AStar-Algorithm with Cache.
    ============================================================================
    """

    def __init__(self,
                 problem: Problem,
                 heuristics: Callable[[Node], int],
                 cache: set[Node],
                 name: str = 'AStar-Cache') -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        self._heuristics = heuristics
        AlgoOneToOneCache.__init__(self,
                                   problem=problem,
                                   type_queue=QueuePriority,
                                   cache=cache,
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
