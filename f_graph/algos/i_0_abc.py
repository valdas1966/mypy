from f_graph.ops.node import OpsNode, Problem, Data, Node
from f_abstract.mixins.nameable import Nameable
from f_abstract.mixins.validatable import Validatable
from typing import Generic
from abc import abstractmethod


class AlgoPathABC(Generic[Problem, Data, Node], Nameable, Validatable):
    """
    ============================================================================
     Base-Class for Path-Algorithms.
    ============================================================================
    """

    def __init__(self,
                 problem: Problem,
                 name: str = None) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        Nameable.__init__(self, name=name)
        Validatable.__init__(self)
        self._problem = problem
        self._data = self._create_data()
        self._ops_node = self._create_ops_node()
        self._search()

    def _create_data(self) -> Data[Node]:
        pass

    def _create_ops_node(self) -> OpsNode[Problem, Data, Node]:
        """
        ========================================================================
         Dependency Injection - Create an Operations-on-Nodes class.
        ========================================================================
        """
        return OpsNode(problem=self._problem, data=self._data)

    @abstractmethod
    def _search(self) -> None:
        """
        ========================================================================
         Execute the search process.
        ========================================================================
        """
        pass
