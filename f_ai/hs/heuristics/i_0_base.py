from f_ai.hs.nodes.i_1_f import NodeF
from typing import Generic, TypeVar, Callable
from abc import ABC, abstractmethod

Node = TypeVar('Node', bound=NodeF)


class HeuristicsBase(ABC, Generic[Node]):
    """
    ============================================================================
     Base-Class for Heuristics.
    ============================================================================
    """

    @abstractmethod
    def eval(self, node: Node) -> int:
        """
        ========================================================================
         Evaluate Heuristic to a given Node.
        ========================================================================
        """
        pass
