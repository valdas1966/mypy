from f_graph.ops.i_0_node_abc import OpsNodeABC, Problem, Data, Node
from f_ds.queues.i_0_base import QueueBase as Queue
from f_abstract.mixins.nameable import Nameable
from f_abstract.mixins.validatable import Validatable
from typing import Generic, TypeVar, Type
from abc import abstractmethod

OpsNode = TypeVar('OpsNode', bound=OpsNodeABC)


class AlgoPathABC(Generic[Problem, OpsNode, Data, Node], Nameable, Validatable):
    """
    ============================================================================
     Base-Class for Path-Algorithms.
    ============================================================================
    """

    def __init__(self,
                 problem: Problem,
                 type_queue: Type[Queue],
                 type_data: Type[Data],
                 type_ops_node: Type[OpsNode],
                 name: str = None) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        Nameable.__init__(self, name=name)
        Validatable.__init__(self)
        self._problem = problem
        self._data = type_data(type_queue=type_queue)
        self._ops_node = type_ops_node(problem=problem, data=self._data)
        self._search()

    @abstractmethod
    def _search(self) -> None:
        """
        ========================================================================
         Execute the search process.
        ========================================================================
        """
        pass
