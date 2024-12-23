from f_graph.path.elements.node import NodePath as Node
from collections import Counter
from typing import Iterable


class StateMulti:
    """
    ============================================================================
     State of Multiple-Goal Path-Algorithms.
    ============================================================================
    """

    def __init__(self) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        self._generated: Counter[Node] = Counter()
        self._explored: Counter[Node] = Counter()

    @property
    def generated(self) -> Counter[Node]:
        """
        ========================================================================
         Return the Counter of all Nodes generated during the Algo-Multi.
        ========================================================================
        """
        return self._generated

    @property
    def explored(self) -> Counter[Node]:
        """
        ========================================================================
         Return the Counter of all Nodes explored during the Algo-Multi.
        ========================================================================
        """
        return self._explored

    def add_generated(self, generated: Iterable[Node]) -> None:
        """
        ========================================================================
         Add Generated-Nodes from previous Iteration.
        ========================================================================
        """
        self._generated.update(generated)

    def add_explored(self, explored: Iterable[Node]) -> None:
        """
        ========================================================================
         Add Explored-Nodes from previous Iteration.
        ========================================================================
        """
        self._explored.update(explored)
