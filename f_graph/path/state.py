from collections.abc import Collection
from f_graph.path.elements.node import NodePath as Node


class StatePath:
    """
    ============================================================================
     State object of the Path-Algorithm.
    ============================================================================
    """

    def __init__(self) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        self._generated: Collection[Node] | None = None
        self._explored: Collection[Node] | None = None
