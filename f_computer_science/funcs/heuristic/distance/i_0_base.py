from f_data_structure.nodes.i_0_base import NodeBase
from typing import Generic, TypeVar
from abc import ABC, abstractmethod

Node = TypeVar('Node', bound=NodeBase)

class Heuristic(ABC, Generic[Node]):
    """
    ============================================================================
     Base-Class for Heuristic Distance-Function.
    ============================================================================
    """

    @abstractmethod
    def calc(self, node: Node) -> int:
        """
        ========================================================================
         Return Heuristic-Distance from Node.
        ========================================================================
        """
        pass
