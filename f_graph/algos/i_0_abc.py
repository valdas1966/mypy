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
                 name: str = None) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        Nameable.__init__(self, name=name)
        Validatable.__init__(self)
        self._type_queue = type_queue
        self._problem = problem
        self._data = self._create_data()
        self._ops_node = self._create_ops_node()
        self._search()

    def _create_data(self) -> Data[Node]:
        pass

    def _create_ops_node(self) -> OpsNodeABC[Problem, Data, Node]:
        """
        ========================================================================
         Dependency Injection - Create an Operations-on-Nodes class.
        ========================================================================
        """
        pass

    @abstractmethod
    def _search(self) -> None:
        """
        ========================================================================
         Execute the search process.
        ========================================================================
        """
        pass
