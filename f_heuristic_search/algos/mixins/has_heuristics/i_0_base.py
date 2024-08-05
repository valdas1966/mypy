from f_data_structure.nodes.i_2_cell import NodeCell
from abc import ABC, abstractmethod
from typing import Generic, TypeVar

Node = TypeVar('Node', bound=NodeCell)


class HasHeuristicsBase(ABC, Generic[Node]):
    """
    ============================================================================
     Base-Class for Algo with Heuristics.
    ============================================================================
    """

    @abstractmethod
    def calc(self, node: Node) -> int:
        """
        ========================================================================
         Return Heuristics-Value for list given Node.
        ========================================================================
        """
        pass