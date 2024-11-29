from f_graph.path_finding.components.path import Path as PathFinding, NodePath
from typing import Generic, TypeVar

Node = TypeVar('Node', bound=NodePath)


class Path(Generic[Node], PathFinding[Node]):

    def __init__(self, cache: set[Node]) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        self._cache = {node: node for node in cache}

    def get(self, goal: Node) -> list[Node]:
        pass
