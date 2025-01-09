from f_graph.path.node import NodePath as Node
from collections.abc import Collection


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

    @property
    def generated(self) -> Collection[Node]:
        return self._generated

    @property
    def explored(self) -> Collection[Node]:
        return self._explored
